from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .constants import PAGINATION
from .forms import CommentForm
from .models import Post, Category
from .mixin import PostMixin, CommentMixin, UserPassesMixin


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


def annotate_comments(post_manager):
    return post_manager.annotate(comment_count=Count('comments')
                                 ).order_by('-pub_date')


class IndexView(ListView):
    template_name = 'blog/index.html'
    paginate_by = PAGINATION
    queryset = filter_posts_by_date(
        annotate_comments(Post.objects)
    )


class PostDetailView(PostMixin, ListView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'
    paginate_by = PAGINATION

    def get_post(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        if not post.is_published and post.author != self.request.user:
            raise Http404("Пост не найден")
        return post

    def get_queryset(self):
        queryset = self.get_post().comments.select_related('author')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_post()
        context['form'] = CommentForm()
        return context


class CreatePostView(PostMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(PostMixin, UserPassesMixin, UpdateView):

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            self.kwargs['post_pk']
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_pk': self.kwargs['post_pk']}
        )

    def test_func(self):
        return self.request.user == self.get_object().author


class DeletePostView(PostMixin, UserPassesMixin, DeleteView):

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            self.kwargs['post_pk']
        )

    def test_func(self):
        return self.request.user == self.get_object().author


class CreateCommentView(CommentMixin, CreateView):
    template_name = 'includes/comments.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post,
            pk=self.kwargs['comment_pk']
        )
        return super().form_valid(form)


class UpdateCommentView(CommentMixin, UserPassesMixin, UpdateView):
    pass


class DeleteCommentView(CommentMixin, UserPassesMixin, DeleteView):
    pass


class CategoryView(ListView):
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category'
    paginate_by = PAGINATION

    def get_category(self):
        category = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs.get('category')
        )
        return category

    def get_queryset(self):
        queryset = filter_posts_by_date(self.get_category().posts.all())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context
