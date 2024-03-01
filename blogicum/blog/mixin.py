from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import CommentForm, PostForm
from .models import Post, Comment


class UserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author


class PostMixin(LoginRequiredMixin):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_pk'
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy(
            'profile',
            kwargs={'username': self.request.user}
        )


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_pk': self.object.post_id}
        )
