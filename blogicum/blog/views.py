from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CreateCommentForm
from .mixins import (CategoryGetMixin, CommentMixin, ListingMixin,
                     PostBaseMixin, PostCategoryAuthorQuerysetMixin,
                     PostEditsMixin, UrlLoginMixin)
from .models import Comment, Post


class PostListView(ListingMixin, PostCategoryAuthorQuerysetMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'


class CreatePostView(LoginRequiredMixin, PostEditsMixin, CreateView):

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(UrlLoginMixin, PostEditsMixin, UpdateView):
    pass


class PostDeleteView(UrlLoginMixin, PostEditsMixin, DeleteView):

    def get_success_url(self):
        return reverse('blog:index')


class PostDetailView(PostBaseMixin, PostCategoryAuthorQuerysetMixin,
                     DetailView):

    template_name = 'blog/detail.html'

    def get_post(self):
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
            post=self.get_post(),
            comments=Comment.objects.select_related('post').filter(
                post=kwargs['object'])
        )


class CategoryListView(ListingMixin, PostCategoryAuthorQuerysetMixin,
                       CategoryGetMixin, ListView):

    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'


class CommentAddView(LoginRequiredMixin, CommentMixin, CreateView):
    pass


class CommentEditView(UrlLoginMixin, CommentMixin, UpdateView):
    pass


class CommentDeleteView(UrlLoginMixin, CommentMixin, DeleteView):
    pass
