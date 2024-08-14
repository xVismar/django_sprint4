from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .forms import CreateCommentForm, CreatePostForm
from .models import Comment, Post


class PostBaseMixin:
    model = Post
    template_name = 'blog/create.html'
    form_class = CreatePostForm
    pk_url_kwarg = 'post_id'


class UserIsPostAuthorMixin(LoginRequiredMixin, UserPassesTestMixin):

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail', self.kwargs[self.pk_url_kwarg]
        )

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=CreatePostForm(instance=get_object_or_404(
                Post.objects,
                pk=self.kwargs[self.pk_url_kwarg])), **kwargs)


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CreateCommentForm
    pk_url_kwarg = 'post_id'
    posts = None

    def get_object(self):
        if self.kwargs.get('comment_id') is not None:
            return get_object_or_404(
                Comment.objects, pk=self.kwargs['comment_id']
            )
        return None

    def dispatch(self, request, *args, **kwargs):
        self.posts = get_object_or_404(
            Post.objects, pk=self.kwargs[self.pk_url_kwarg]
        )

        if self.get_object() and self.get_object().author != self.request.user:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', args=[self.kwargs[self.pk_url_kwarg]]
        )
