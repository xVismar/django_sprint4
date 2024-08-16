from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CreateCommentForm, EditUserProfileForm
from .mixins import CommentMixin, PostBaseMixin, UserIsPostAuthorMixin
from .models import Category, Comment, Post, User

PAGINATE_BY = 10


def get_posts(
    posts=Post.objects, get_related=True, filter_published=True, annotate=True
):
    if get_related:
        posts = posts.select_related('author', 'category', 'location')
    if filter_published:
        posts = posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
    if annotate:
        posts = posts.annotate(
            comment_count=Count('comments')
        ).order_by(*Post._meta.ordering)
    return posts


class PostListView(ListView):
    model = Post
    paginate_by = PAGINATE_BY
    template_name = 'blog/index.html'

    def get_queryset(self):
        return get_posts()


class PostCreateView(LoginRequiredMixin, PostBaseMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class PostEditView(UserIsPostAuthorMixin, PostBaseMixin, UpdateView):
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            args=[self.kwargs[self.pk_url_kwarg]]
        )


class PostDeleteView(UserIsPostAuthorMixin, PostBaseMixin, DeleteView):
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        if post.author != self.request.user:
            return get_object_or_404(
                get_posts(annotate=False, get_related=False),
                pk=self.kwargs[self.pk_url_kwarg]
            )
        return post

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=CreateCommentForm(),
            comments=self.get_object().comments.get_queryset(),
            **kwargs
        )


class CategoryListView(ListView):
    model = Post
    paginate_by = PAGINATE_BY
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs[self.slug_url_kwarg],
            is_published=True
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(category=self.get_category(), **kwargs)

    def get_queryset(self):
        return get_posts(posts=self.get_category().posts, )


class CommentAddView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', args=[self.kwargs['post_id']]
        )


class CommentEditView(LoginRequiredMixin, CommentMixin, UpdateView):

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=CreateCommentForm(instance=self.get_object()),
            post=get_object_or_404(Post, pk=self.kwargs['post_id']),
            **kwargs
        )


class CommentDeleteView(CommentMixin, DeleteView):
    pass


class ProfileView(ListView):
    template_name = 'blog/profile.html'
    model = Post
    paginate_by = PAGINATE_BY

    def get_author(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username']
        )

    def get_queryset(self):
        author = self.get_author()
        return get_posts(
            posts=author.posts,
            filter_published=True if author != self.request.user else False
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            profile=self.get_author(),
            **kwargs
        )


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = EditUserProfileForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])
