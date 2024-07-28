from blog.models import Category, Post

from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from core.mixins import OnlyAuthorMixin

from django.urls import reverse_lazy
from django.http import request

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)


from .forms import PostForm, CommentForm, CategoryForm

DISP_LIMIT = 10


class PostListView(ListView):
    model = Post
    queryset = Post.posts()
    ordering = '-pub_date'
    paginate_by = DISP_LIMIT
    template_name = 'blog/index.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
  


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentaryForm()
        context['comments'] = (
            self.object.commentary.select_related('author')
        )
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    pass


class CommentEditView(LoginRequiredMixin, UpdateView,):
    pass


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    pass


class CategoryListView(ListView):
    model = Category
    queryset = Post.posts().select_related('category')
    ordering = '-pub_date'
    paginate_by = DISP_LIMIT
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = (
            self.objects.filter(slug=category_slug)
        )
        return context