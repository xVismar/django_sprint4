from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CreateCommentForm
from .mixins import CommentMixin, PostBaseMixin, UserIsPostAuthorMixin
from .models import Category, Comment, Post


PAGINATE_BY = 10


def get_posts(
    posts=Post.objects, filter_published=False, filter_category=False,
    filter_author=False, annotate=False, pk=None, slug=None, username=None
):

    def annotate_order(self):
        return self.annotate(
            comment_count=Count('comments')
        ).order_by(*Post._meta.ordering)

    def published(self):
        return self.filter(is_published=True, pub_date__lte=timezone.now())

    category_posts = posts.select_related('category').filter(
        category__is_published=True
    )

    author_posts = posts.select_related('author', 'category').filter(
        author__username=username
    )

    if filter_published:
        return annotate_order(published(category_posts))

    if pk and not filter_published:
        return get_object_or_404(posts, pk=pk)

    if slug:
        if not filter_category:
            return get_object_or_404(Category, slug=slug, is_published=True)
        return annotate_order(published(category_posts).filter(
            category__slug=slug,)
        )

    if username:
        if not filter_author:
            return annotate_order(author_posts)
        return annotate_order(
            published(author_posts.filter(category__is_published=True))
        )


class PostListView(ListView):
    model = Post
    paginate_by = PAGINATE_BY
    template_name = 'blog/index.html'

    def get_queryset(self):
        return get_posts(filter_published=True, annotate=True)


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
        post = get_posts(pk=self.kwargs[self.pk_url_kwarg])
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
            comments=self.get_object().comments.get_queryset(),
            **kwargs
        )


class CategoryListView(ListView):
    model = Post
    paginate_by = PAGINATE_BY
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            category=get_posts(slug=self.kwargs[self.slug_url_kwarg])
        )

    def get_queryset(self):
        return get_posts(
            filter_category=True,
            slug=self.kwargs[self.slug_url_kwarg],
        )


class CommentAddView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_posts(pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', args=[self.kwargs['post_id']]
        )


class CommentEditView(LoginRequiredMixin, CommentMixin, UpdateView):

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=CreateCommentForm(instance=self.get_object()),
            post=get_posts(pk=self.kwargs['post_id']),
            **kwargs
        )


class CommentDeleteView(CommentMixin, DeleteView):
    pass
