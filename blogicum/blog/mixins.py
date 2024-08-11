from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from .forms import CreateCommentForm, CreatePostForm
from .models import Category, Comment, Post


class CreateUpdateView(
        SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    model = Post
    template_name = 'blog/create.html'
    form_class = CreatePostForm
    pk_url_kwarg = 'post_id'


class PostBaseMixin:
    model = Post
    pk_url_kwarg = 'post_id'

    class Meta:
        abstract = True


class PostEditsMixin(PostBaseMixin):
    template_name = 'blog/create.html'
    form_class = CreatePostForm

    def get_context_data(self):
        if self.kwargs.get('post_id') is not None:
            return super().get_context_data(form=CreatePostForm(
                instance=Post.objects.get(pk=self.kwargs[self.pk_url_kwarg])
            ))

        return super().get_context_data(form=CreatePostForm(instance=None))


class UrlLoginMixin(LoginRequiredMixin, UserPassesTestMixin):

    def get_success_url(self):
        if self.kwargs.get('post_id') is not None:
            return reverse(
                'blog:post_detail',
                kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
            )

        return reverse('blog:profile', args=self.request.user.username)

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail', self.kwargs[self.pk_url_kwarg]
        )

    def test_func(self):
        return self.request.user == self.get_object().author


class PostCategoryAuthorQuerysetMixin:

    def get_queryset(self):
        queryset = Post.objects.select_related(
            'author',
            'category',
            'location',
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')

        if hasattr(self, 'pk_url_kwawrg'):
            if self.pk_url_kwarg == 'post_id':
                queryset = queryset.filter(
                        category__is_published=True,
                        is_published=True,
                        pub_date__lte=timezone.now())

            if self.pk_url_kwarg == 'comment_id':
                queryset = Comment.objects.filter(pk=self.kwargs['comment_id'])

            return queryset

        if hasattr(self, 'slug_url_kwarg'):
            if self.slug_url_kwarg == 'category_slug':
                queryset = queryset.filter(
                    category__is_published=True,
                    is_published=True,
                    pub_date__lte=timezone.now(),
                    category__slug=self.kwargs[self.slug_url_kwarg])

            if self.slug_url_kwarg == 'username':
                queryset = queryset.filter(
                    author__username=self.kwargs[self.slug_url_kwarg])

            return queryset

        return queryset.filter(
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now())


class ListingMixin:
    model = Post
    paginate_by = 10



class CategoryGetMixin:

    def get_context_data(self):
        return super().get_context_data(
            category=get_object_or_404(
                Category,
                slug=self.kwargs[self.slug_url_kwarg],
                is_published=True)
        )


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CreateCommentForm
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get('comment_id') is not None:
            comment = self.get_object()

            if self.request.user != comment.author:
                return redirect(
                    'blog:post_detail',
                    args=self.kwargs['post_id']
                )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = get_object_or_404(Post.objects, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)
