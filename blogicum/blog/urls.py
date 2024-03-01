from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('',
         views.IndexView.as_view(),
         name='index'),
    path('posts/<int:post_pk>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/create/',
         views.CreatePostView.as_view(),
         name='create_post'),
    path('posts/<int:post_pk>/edit/',
         views.UpdatePostView.as_view(),
         name='edit_post'),
    path('posts/<int:post_pk>/delete/',
         views.DeletePostView.as_view(),
         name='delete_post'),
    path('posts/<int:comment_pk>/comment/',
         views.CreateCommentView.as_view(),
         name='add_comment'),
    path('posts/<int:post_pk>/edit_comment/<int:comment_pk>',
         views.UpdateCommentView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_pk>/delete_comment/<int:comment_pk>',
         views.DeleteCommentView.as_view(),
         name='delete_comment'),
    path('category/<slug:category>/',
         views.CategoryView.as_view(),
         name='category_posts'),
]
