from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CreateCommentForm
from .mixins import CommentMixin, PostBaseMixin, UserIsAuthorMixin
from .models import Category, Comment, Post


def post_category_profile_queryset(self, category_slug=None, username=None):

    general_posts = Post.objects.select_related('category').filter(
        category__is_published=True,
        is_published=True,
        pub_date__lte=timezone.now()
    )

    if category_slug is not None:
        category_posts = general_posts.filter(category__slug=category_slug)
        return category_posts.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    if username is not None:
        author_posts = Post.objects.select_related('author').filter(
            author__username=username)

        return author_posts.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    return general_posts.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_queryset(self):
        return post_category_profile_queryset(self)


class PostCreateView(PostBaseMixin, CreateView):

    def get_success_url(self):
        return reverse(
            'blog:profile', args=[self.request.user]
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(UserIsAuthorMixin, PostBaseMixin, UpdateView):

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            args=[self.kwargs[self.pk_url_kwarg]]
        )


class PostDeleteView(UserIsAuthorMixin, PostBaseMixin, DeleteView):

    def get_success_url(self):
        return reverse('blog:index')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        post = get_object_or_404(
            Post,
            pk=self.kwargs[self.pk_url_kwarg]
        )
        if self.request.user == post.author:
            return post
        return get_object_or_404(
            Post.objects.filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                category__is_published=True,
            ),
            pk=self.kwargs[self.pk_url_kwarg],
        )

    def get_context_data(self, **kwargs):

        return super().get_context_data(
            form=CreateCommentForm(),
            post=self.get_object(),
            comments=Comment.objects.filter(post=self.get_object())
        )


class CategoryListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            category=get_object_or_404(
                Category,
                slug=self.kwargs[self.slug_url_kwarg],
                is_published=True)
        )

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return post_category_profile_queryset(self, category_slug)


class CommentAddView(CommentMixin, CreateView):
    pass


class CommentEditView(CommentMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, DeleteView):
    pass
