from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CreateCommentForm, CreatePostForm
from .mixins import (
    CommentMixin,
    CreateUpdateView,
    ListingMixin,
    PostFieldsMixin,
    UrlLoginMixin,
)
from .models import Category, Comment, Post


class PostListView(ListingMixin, ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        return (
            super(PostListView, self)
            .get_queryset()
            .filter(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True,
            )
        )


class CreateEditPostView(UrlLoginMixin, PostFieldsMixin, CreateUpdateView):
    pk_url_kwarg = 'post_id'
    form_class = CreatePostForm

    def dispatch(self, request, *args, **kwargs):

        if self.get_object() is None:
            return super().dispatch(request, *args, **kwargs)
        else:
            if self.get_object().author != self.request.user:
                return redirect(
                    'blog:post_detail', post_id=self.kwargs['post_id']
                )
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(UrlLoginMixin, PostFieldsMixin, DeleteView):
    pk_url_kwarg = 'post_id'

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post.objects, pk=self.kwargs['post_id'])
        if self.request.user != post.author:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:index')


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
        return (super(CategoryListView, self).get_queryset().filter(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__slug=self.kwargs['category_slug']
                ))

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(kwargs={'category': get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True)}
        )


class CommentAddView(UrlLoginMixin, CommentMixin, CreateView):
    pass


class CommentEditView(UrlLoginMixin, CommentMixin, UpdateView):
    pass


class CommentDeleteView(UrlLoginMixin, CommentMixin, DeleteView):
    pass
