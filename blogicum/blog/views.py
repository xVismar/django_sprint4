from blog.models import Category, Post

from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin, OnlyAuthorMixin

from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)


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
    success_url = reverse_lazy('blog:profile/', request.POST.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(OnlyAuthorMixin, UpdateView, LoginRequiredMixin):
    model = Birthday
    form_class = BirthdayForm



class PostDeleteView(LoginRequiredMixin, DeleteView, OnlyAuthorMixin):
    model = Post
    success_url = reverse_lazy('birthday:list')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentaryForm()
        context['comments'] = (
            self.object.commentary.select_related('author')
        )
        return context







def post_detail(request, id):
    context = {'post': get_object_or_404(Post.posts(), pk=id)}
    template = 'blog/detail.html'
    return render(request, template, context)


def category_posts(request, category_slug):

    category = get_object_or_404(
        Category.objects.published(),
        slug=category_slug
    )
    post = Post.objects.select_related('category').filter(
        category=category).check_pub_time()

    context = {'category': category, 'post_list': post}
    template = 'blog/category.html'
    return render(request, template, context)

