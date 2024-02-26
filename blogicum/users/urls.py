from django.urls import path

from . import views


urlpatterns = [
    path('auth/registration/', views.CreateUserView.as_view(),
         name='registration'),
    path('profile/edit/<int:pk>/', views.UserUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<str:username>/', views.profile_user,
         name='profile'),
]
