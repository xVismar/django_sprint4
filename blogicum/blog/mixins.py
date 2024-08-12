from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from .forms import CreateCommentForm, CreatePostForm
from .models import Comment, Post


class PostBaseMixin:
    model = Post
    template_name = 'blog/create.html'
    form_class = CreatePostForm
    pk_url_kwarg = 'post_id'


class UserIsAuthorMixin(UserPassesTestMixin):

    def handle_no_permission(self):
        return HttpResponseRedirect(
            reverse_lazy(
                'blog:post_detail',
                args=[self.kwargs[self.pk_url_kwarg]]
            ))

    def test_func(self):
        post_author = self.get_object().author
        return self.request.user == post_author

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=CreatePostForm(instance=get_object_or_404(
                Post.objects,
                pk=self.kwargs[self.pk_url_kwarg])), **kwargs)

class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CreateCommentForm
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get('comment_id') is not None:
            comment = self.get_object()

            if self.request.user != comment.author:
                return HttpResponseRedirect(
                    'blog:post_detail',
                    self.kwargs['post_id'])

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post.objects,
            pk=self.kwargs['post_id']
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])
