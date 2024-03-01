from django.urls import path

from . import views


urlpatterns = [
    path('auth/registration/', views.CreateUserView.as_view(),
         name='registration'),
    path('profile/edit/<slug:username>/', views.UserUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<slug:username>/', views.ProfileView.as_view(),
         name='profile'),
]
