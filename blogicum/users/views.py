from blog.models import Post
from core.mixins import ListingMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView

User = get_user_model()


class ProfileView(ListingMixin, ListView):
    template_name = 'blog/profile.html'
    queryset = Post.objects.select_related('author')

    def get_queryset(self):
        author = self.get_profile_object()
        queryset = super().get_queryset().filter(author=author)
        if author != self.request.user:
            queryset = queryset.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            )

        return queryset.annotate(comment_count=Count('comments'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_profile_object()
        context['profile'] = author
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
        profile = get_object_or_404(User.objects, username=self.request.user)
        return profile

    def get_success_url(self, *args, **kwargs):
        return reverse('blog:profile', kwargs={'username': self.request.user})
