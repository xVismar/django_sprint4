from django.urls import path

from . import views
import users.views as user_views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),

    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(), name='post_detail'
         ),

    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(), name='category_posts'
         ),

    path('posts/create/',
         views.CreateEditPostView.as_view(), name='create_post'
         ),

    path('posts/<int:post_id>/edit/',
         views.CreateEditPostView.as_view(), name='edit_post'
         ),

    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'
         ),

    path('posts/<int:post_id>/comment/',
         views.CommentAddView.as_view(), name='add_comment'
         ),

    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentEditView.as_view(), name='edit_comment'
         ),

    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(), name='delete_comment'
         ),

    path('profile/<slug:username>/',
         user_views.ProfileView.as_view(), name='profile'),

    path('edit_profile/',
         user_views.EditProfileView.as_view(), name='edit_profile')
]
