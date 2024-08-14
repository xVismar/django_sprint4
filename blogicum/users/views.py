from blog.models import Post, User
from blog.views import get_posts

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, UpdateView


class ProfileView(ListView):
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    model = Post
    paginate_by = 10

    def get_queryset(self):
        return get_posts(
            Post.objects,
            username=self.kwargs[self.slug_url_kwarg],
            is_profile=True
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            profile=get_object_or_404(
                User.objects, username=self.kwargs[self.slug_url_kwarg]),
            **kwargs
        )


class EditProfileView(UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]

    def get_object(self):
        return get_object_or_404(
            User.objects,
            username=self.request.user.username
        )

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])
