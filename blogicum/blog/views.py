from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from core.mixins import (
    CommentMixin,
    CreateUpdateView,
    ListingMixin,
    PostFieldsMixin
)
from .forms import CreateCommentForm, CreatePostForm
from .models import Category, Comment, Post

User = get_user_model()


class PostListView(ListingMixin, ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        qs = Post.objects.select_related('category').exclude(
            pub_date__gt=timezone.now()).filter(
                is_published=True,
                category__is_published=True).order_by('-pub_date').annotate(
                    comment_count=Count('comments'))
        return qs


class CreateEditPostView(LoginRequiredMixin, PostFieldsMixin,
                         CreateUpdateView):

    fields = [
        'title',
        'pub_date',
        'text',
        'category',
        'location',
        'image'
    ]

    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if 'edit/' in self.request.path:
            post = self.get_post_object()
            if self.request.user != post.author:
                return HttpResponseRedirect(reverse(
                    'blog:post_detail',
                    kwargs={'post_id': self.kwargs['post_id']}
                ))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super(CreateEditPostView, self).get_context_data(**kwargs)
        if 'edit/' not in self.request.path:
            instance = None
            context['form'] = CreatePostForm(instance=instance)
            return context

        instance = self.get_post_object()
        context['form'] = CreatePostForm(instance=instance)
        return context


class PostDeleteView(LoginRequiredMixin, PostFieldsMixin, DeleteView):
    pk_url_kwarg = 'post_id'

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteView, self).get_context_data(*args, **kwargs)
        instance = self.get_post_object()
        context['form'] = CreatePostForm(instance=instance)
        return context

    def delete(self, request, *args, **kwargs):
        post = self.get_post_object()
        if self.request.user != post.author:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().delete(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        author = get_object_or_404(Post, pk=self.kwargs['post_id']).author

        if self.request.user != author:
            queryset = queryset.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            )
        return queryset

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            raise Http404('Такого поста не существует.')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateCommentForm()
        context['comments'] = Comment.objects.select_related('post').filter(
            post_id=self.kwargs['post_id']
        )

        return context


class CategoryListView(ListingMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return (
            queryset.select_related('category').filter(
                pub_date__lte=timezone.now(),
                category__slug=self.kwargs['category_slug'],
                is_published=True
            ).annotate(comment_count=Count('comments'))
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

        return context


class CommentAddView(LoginRequiredMixin, CommentMixin, CreateView):
    pass


class CommentEditView(LoginRequiredMixin, CommentMixin, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(CommentEditView, self).get_context_data(**kwargs)
        instance = get_object_or_404(
            Comment.objects,
            pk=self.kwargs['comment_id']
        )
        context['form'] = CreateCommentForm(instance=instance)
        return context


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    context_object_name = 'comment'
