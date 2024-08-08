
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from .forms import CreateCommentForm, CreatePostForm
from .models import Comment, Post


class CreateUpdateView(
        SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView
):

    def get_object(self, queryset=None):
        if self.kwargs.get('post_id') is not None:
            return get_object_or_404(Post, pk=self.kwargs['post_id'])
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.request.user:
            self.object = self.get_object()
            return super(CreateUpdateView, self).post(request, *args, **kwargs)


class PostFieldsMixin:
    model = Post
    template_name = 'blog/create.html'


class UrlLoginMixin(LoginRequiredMixin):

    def get_success_url(self):
        if self.kwargs.get('post_id') is not None:
            return reverse(
                'blog:post_detail',
                kwargs={'post_id': self.kwargs['post_id']}
            )

        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )

    def get_context_data(self, **kwargs):
        if self.kwargs.get('post_id') is not None:
            return super().get_context_data(
                kwargs={'form': CreatePostForm(
                    instance=get_object_or_404(
                        Post.objects,
                        pk=self.kwargs['post_id']))}
            )

        elif self.kwargs.get('comment_id') is not None:
            return super().get_context_data(
                kwargs={'form': CreateCommentForm(
                    instance=get_object_or_404(
                        Comment.objects,
                        pk=self.kwargs['comment_id']))}
            )

        return super().get_context_data(
            kwargs={'form': CreatePostForm(instance=None)}
        )


class ListingMixin:
    model = Post
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        return super(ListingMixin, self).get_queryset().annotate(
            comment_count=Count('comments')
        )


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CreateCommentForm
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        if not self.kwargs.get('comment_id'):
            return super().dispatch(request, *args, **kwargs)

        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        if self.request.user != comment.author:
            return HttpResponseRedirect(reverse(
                'blog:post_detail',
                kwargs={'post_id': self.kwargs['post_id']})
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)
