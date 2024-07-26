from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/create', views.POST CREATE VIEWS, name='post_create'),
    path('posts/<int:post_id>/edit/', views.POST EDIT VIEWS, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.POST DELETE VIEWS, name='post_delete'),
    path('posts/<int:id>/', views. POST DETAIL VIEWS, name='post_detail'),
    path('profile/<username>', views.PROFILE VIEWS, name='profile'),
     path('posts/<int:post_id>/create_comment/',
        views.CommentCreate.as_view(), name='comment_create'),
    path('posts/<post_id>/edit_comment/<int:comment_id>/',
        views.CommentEdit.as_view(), name='comment_edit'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.CommentDelete.as_view(), name='comment_delete'),
    path('category/<slug:category_slug>/', views. CATEGORY POSTS VIEWS,
         name='category_posts'),
]