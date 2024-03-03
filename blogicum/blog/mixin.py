from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import CommentForm, PostForm
from .models import Post, Comment


class UserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author


class PostMixin(UserPassesMixin, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_pk'
    template_name = 'blog/post_form.html'

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            self.kwargs.get(
                self.pk_url_kwarg)
        )

    def get_success_url(self):
        return reverse(
            'profile',
            kwargs={'username': self.request.user}
        )


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_pk': self.object.post_id}
        )
