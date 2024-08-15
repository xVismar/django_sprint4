from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CreateCommentForm
from .mixins import CommentMixin, PostBaseMixin, UserIsPostAuthorMixin
from .models import Comment, Post


PAGINATE_BY = 10


def get_posts(
    posts=Post.objects, filter_published=True, filter_category=False,
    filter_author=False, annotate=True
):

    if filter_category:
        return posts.select_related('category').filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        ).annotate(comment_count=Count('comments')
                   ).order_by(*Post._meta.ordering)

    if filter_author:
        if not filter_published:
            return posts.select_related('author').annotate(
                comment_count=Count('comments')
            ).order_by(*Post._meta.ordering)

        return posts.select_related('author').filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        ).annotate(comment_count=Count('comments')
                   ).order_by(*Post._meta.ordering)

    if annotate is False:
        if not filter_published:
            return posts
        return posts.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        )

    return posts.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).annotate(comment_count=Count('comments')
               ).order_by(*Post._meta.ordering)


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
        post = super().get_object()
        if not post.is_published and post.author != self.request.user:
            raise Http404
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

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            category=get_object_or_404(
                Post.category.get_queryset().filter(
                    is_published=True,
                    slug=self.kwargs['category_slug'])
            )
        )

    def get_queryset(self):
        return get_posts(
            posts=Post.category.get_queryset().filter(
                slug=self.kwargs['category_slug']).first(
            ).posts.get_queryset(),
            filter_category=True
        )


class CommentAddView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Comment.post.get_queryset(),
            pk=self.kwargs['post_id']
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', args=[self.kwargs['post_id']]
        )


class CommentEditView(LoginRequiredMixin, CommentMixin, UpdateView):

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=CreateCommentForm(instance=self.get_object()),
            post=get_object_or_404(
                Comment.post.get_queryset(),
                pk=self.kwargs['post_id']),
            **kwargs
        )


class CommentDeleteView(CommentMixin, DeleteView):
    pass
