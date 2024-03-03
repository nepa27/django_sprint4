from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, ListView
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy

from blog.constants import PAGINATION
from blog.views import annotate_comments, filter_posts_by_date

User = get_user_model()


class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:index')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = (
        'username',
        'email',
        'first_name',
        'last_name'
    )
    template_name = 'users/user_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse(
            'profile',
            kwargs={'username': self.request.user.username}
        )

    def test_func(self):
        return self.request.user.username == self.kwargs['username']


class ProfileView(ListView):
    model = User
    template_name = 'users/profile.html'
    paginate_by = PAGINATION
    slug_url_kwarg = 'username'

    def get_profile(self):
        profile = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return profile

    def get_queryset(self):
        queryset = annotate_comments(self.get_profile().posts)
        if self.request.user.username != self.kwargs['username']:
            return filter_posts_by_date(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context
