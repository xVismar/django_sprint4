from django.urls import path
from users import views as user_views
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/create', views.CreatePostView.as_view(), name='create_post'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('posts/<int:pk>/comment', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/edit_comment/<int:id>/', views.add_comment, name='edit_comment'),
    path('posts/<int:pk>/delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('posts/category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('profile/<username>', user_views.profile, name='profile'),
    path('edit_profile', user_views.edit_profile, name='edit_profile'),

]
