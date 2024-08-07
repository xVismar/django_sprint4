from blog.forms import CreateCommentForm
from blog.models import Comment, Post

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

User = get_user_model()


class CreateUpdateView(
        SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView
):

    def get_object(self, queryset=None):
        pk = self.kwargs.get('post_id')
        if pk is not None:
            return get_object_or_404(Post.objects, pk=self.kwargs['post_id'])
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.request.user:
            self.object = self.get_object()
            return super(CreateUpdateView, self).post(request, *args, **kwargs)

    def get_post_object(self):
        post = get_object_or_404(Post.objects, pk=self.kwargs['post_id'])
        return post


class PostFieldsMixin:
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def check_if_user_is_author(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        if self.request.user != post.author:
            return redirect('blog:post_detail', post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_post_object(self):
        post = get_object_or_404(Post.objects, pk=self.kwargs['post_id'])
        return post


class ListingMixin:
    model = Post
    ordering = '-pub_date'
    paginate_by = 10

    def get_profile_object(self):
        post = get_object_or_404(
            User.objects,
            username=self.kwargs['username']
        )
        return post


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CreateCommentForm
    pk_url_kwarg = 'comment_id'

    def form_valid(self, form):
        if 'delete/' not in self.request.path:
            post = get_object_or_404(
                Post, pk=self.kwargs.get('post_id') or self.kwargs['post_id']
            )
            form.instance.author = self.request.user
            form.instance.post = post
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        if '/comment/' not in self.request.path:
            comment = get_object_or_404(
                Comment, pk=self.kwargs['comment_id']
            )
            if self.request.user != comment.author:
                return HttpResponseRedirect(reverse(
                    'blog:post_detail',
                    kwargs={'post_id': self.kwargs['post_id']})
                )

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
