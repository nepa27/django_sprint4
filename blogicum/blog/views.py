from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import CommentForm, PostForm
from .models import Post, Category, Comment

User = get_user_model()


class PostMixin:
    model = Post
    form_class = PostForm


class IndexView(LoginRequiredMixin, PostMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        queryset = filter_posts_by_date(queryset)
        return queryset


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                Q(author=self.request.user) | Q(is_published=True)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CreatePostView(LoginRequiredMixin, PostMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'profile',
            kwargs={'username': self.request.user}
        )


class UpdatePostView(LoginRequiredMixin, PostMixin,
                     UpdateView):
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )

    def form_valid(self, form):
        if form.instance.author != self.request.user:
            return redirect(
                'blog:post_detail',
                self.kwargs['pk']
            )

        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin,
                     PostMixin, DeleteView):
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        return self.request.user == self.get_object().author


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = 'includes/comments.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.object.post_id}
        )


class CreateCommentView(CommentMixin, LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)


class UpdateCommentView(CommentMixin, LoginRequiredMixin, UpdateView):
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        if form.instance.author != self.request.user:
            return redirect(
                'blog:post_detail',
                self.kwargs['post_pk']
            )
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return super().form_valid(form)


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin,
                        CommentMixin, DeleteView):
    template_name = 'blog/comment.html'

    def test_func(self):
        return self.request.user == self.get_object().author


def filter_posts_by_date(post_manager):
    return post_manager.select_related(
        'author',
        'location',
        'category'
    ).filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    )


def category_post(request, category_slug):
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )

    post = filter_posts_by_date(category.posts.all())
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/category.html',
        {'page_obj': page_obj,
         'category': category}
    )
