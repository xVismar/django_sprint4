from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'blog'

urlpatterns = [
    path('',
         views.PostListView.as_view(),
         name='index'),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'
         ),
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'
         ),
    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'
         ),
    path('posts/<int:post_id>/edit/',
         views.PostEditView.as_view(),
         name='edit_post'
         ),
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'
         ),
    path('posts/<int:post_id>/comment/',
         views.CommentAddView.as_view(),
         name='add_comment'
         ),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentEditView.as_view(),
         name='edit_comment'
         ),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'
         ),
    path('profile/<str:username>/',
         views.ProfileView.as_view(),
         name='profile'
         ),
    path('edit_profile/',
         views.EditProfileView.as_view(),
         name='edit_profile'
         ),
    path('auth/password_change/',
         auth_views.PasswordChangeView.as_view(
             success_url=reverse_lazy('users:password_change_done')),
         name='password_change'
         ),
    path('auth/password_reset/',
         auth_views.PasswordResetView.as_view(
             success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'
         ),
    path('auth/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm',
         )
]
