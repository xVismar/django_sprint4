from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, UpdateView

from blog.mixins import ListingMixin
from blog.models import User


class ProfileView(ListingMixin, ListView):
    template_name = 'blog/profile.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            author__username=self.kwargs['username']
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User.objects,
            username=self.kwargs['username']
        )

        return context


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

    def get_success_url(self, *args, **kwargs):
        return reverse('blog:profile', kwargs={'username': self.request.user})
