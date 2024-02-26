from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin)
from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from blog.models import Post

User = get_user_model()


class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:index')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = [
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    template_name = 'users/user_form.html'

    def get_success_url(self):
        return reverse_lazy(
            'profile',
            kwargs={'username': self.request.user}
        )

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']


def profile_user(request, username):
    profile = get_object_or_404(
        User,
        username=username
    )
    post = Post.objects.filter(
        author=profile
    ).annotate(comment_count=Count(
        'comments', )
    ).order_by('-pub_date')
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'users/profile.html',
        {'profile': profile,
         'page_obj': page_obj}
    )
