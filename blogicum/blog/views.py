from re import L
from blog.models import Category, Post, Comment
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from core.mixins import OnlyAuthorMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from .forms import AddCommentForm, CategoryForm, CreatePostForm, PostDetailForm
from django.core.paginator import Paginator

DISP_LIMIT = 10


class PostListView(ListView):
    model = Post
    queryset = Post.objects.select_related('category').filter(pub_date__lte=timezone.now(), is_published=True, category__is_published=True)
    ordering = '-pub_date'
    paginate_by = DISP_LIMIT
    template_name = 'blog/index.html'
    context_object_name = 'post'


class CreatePostView(CreateView):
    model = Post
    # form_class = CreatePostForm
    template_name = 'blog/create.html'
    fields = '__all__'
    success_url = reverse_lazy('blog:index')

class EditPostView(UpdateView, OnlyAuthorMixin):
    model = Post
    # form_class = CreatePostForm
    template_name = 'blog/create.html'
    fields = ['title', 'pub_date', 'text', 'category', 'location', 'image']
    success_url = reverse_lazy('blog:index')

# def create_post(request, pk=None):
#     if pk is not None:
#         instance = get_object_or_404(Post.objects, pk=pk)
#         form = CreatePostForm(request.POST or None, instance=instance)
#         context = {'form': form, 'instance': instance}
#         if form.is_valid():
#             form.save()
#             return redirect('blog:post_detail', pk=pk)
#         return render(request, 'blog/create.html', context)

#     else:
#         form = CreatePostForm(request.GET)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = form.cleaned_data['author']
#             post.text = form.cleaned_data['text']
#             post.category = form.cleaned_data['category']
#             post.location = form.cleaned_data['locaiton']
#             post.image = form.cleaned_data['image']
#             post.pub_date = form.cleaned_data['pub_date']
#             post.save()
#             return redirect('blog:profile', username=request.user)

        # return render(request, 'blog/create.html', {'form': form})


def edit_post():
    pass
class PostDeleteView(OnlyAuthorMixin, DeleteView):
    pass


def post_detail(request, pk):
    posts = get_object_or_404(Post.objects.all(), pk=pk)
    comments = Comment.objects.select_related('post').filter(post__pk=pk)
    template = 'blog/detail.html'
    form = AddCommentForm
    context = {'post': posts, 'form': form, 'comments': comments}
    return render(request, template, context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects, slug=category_slug)
    posts = Post.objects.select_related('category').filter(
        category=category, is_published=True, category__is_published=True).order_by('-pub_date')

    template = 'blog/category.html'
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}

    return render(request, template, context)


def add_comment(request, pk, id=None):
    post = get_object_or_404(Post.objects, pk=pk)

    if id is not None:
        instance = get_object_or_404(Comment.objects, pk=id)
        form = AddCommentForm(request.POST or None, instance=instance)
        context = {'form': form, 'comment': instance}
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=pk)
        return render(request, 'blog/comment.html', context)

    else:
        form = AddCommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.text = form.cleaned_data['text']
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=pk)


def delete_comment(request, pk, id):
    instance = get_object_or_404(Comment.objects, pk=id)
    form = AddCommentForm(instance=instance)
    context = {'form': form, 'comment': instance}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', pk=pk)

    return render(request, 'blog/comment.html', context)
