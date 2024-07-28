from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [

    path('registration/', views.UserRegistView.as_view(), name='registration'),
    path('profile/<username>', views.ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
]
