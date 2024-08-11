from blog.mixins import ListingMixin, PostCategoryAuthorQuerysetMixin
from blog.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, UpdateView


class ProfileView(ListingMixin, PostCategoryAuthorQuerysetMixin, ListView):
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            profile=get_object_or_404(
                User.objects,
                username=self.kwargs[self.slug_url_kwarg]))


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]

    def get_object(self):
        return get_object_or_404(User.objects, username=self.request.user)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})
