from django.urls import path
from django.contrib.auth.decorators import login_required
import users.views as user_views
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
         login_required(views.PostCreateView.as_view()),
         name='create_post'
         ),
    path('posts/<int:post_id>/edit/',
         login_required(views.PostEditView.as_view()),
         name='edit_post'
         ),
    path('posts/<int:post_id>/delete/',
         login_required(views.PostDeleteView.as_view()),
         name='delete_post'
         ),
    path('posts/<int:post_id>/comment/',
         login_required(views.CommentAddView.as_view()),
         name='add_comment'
         ),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         login_required(views.CommentEditView.as_view()),
         name='edit_comment'
         ),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         login_required(views.CommentDeleteView.as_view()),
         name='delete_comment'
         ),
    path('profile/<str:username>/',
         user_views.ProfileView.as_view(),
         name='profile'),
    path('edit_profile/',
         login_required(user_views.EditProfileView.as_view()),
         name='edit_profile')
]
