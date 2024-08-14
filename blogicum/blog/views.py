from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CreateCommentForm
from .mixins import CommentMixin, PostBaseMixin, UserIsPostAuthorMixin
from .models import Category, Comment, Post, User

# Paginator
PAGES_LIMIT = 10


def get_posts(posts, **kwargs):
    """Функция для получения queryset, без select_related."""
    general_posts = posts.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )

    def annotate_order(self):
        return self.annotate(
            comment_count=Count('comments')
        ).order_by(Post._meta.ordering[0])

    # Получаем post.pk и category.id из фильтрованного списка объектов
    post_id_cat_id = general_posts.values_list('id', 'category_id')
    # Получаем category.id и category.is_published через related_name
    category_id_published = Post.category.get_queryset(
    ).values_list('pk', 'is_published')  # Получем

    category_published = []

    # Через первый цикл распаковываем queryset
    for post_id, cat_id in post_id_cat_id:
        # Внутренним циклом распаковываем второй queryset
        for category_id, published in category_id_published:
            # Сравниваем категорию и статус опубликовано и добавляем в список
            if category_id == cat_id and published is True:
                category_published.append(post_id)

    if 'is_index' in kwargs and kwargs['is_index'] is not None:
        return annotate_order(general_posts.filter(
            id__in=category_published
        ))

    if 'is_category' in kwargs and kwargs['is_category']:
        return annotate_order(general_posts.filter(
            id__in=category_published,
            category__slug=kwargs['category_slug']
        ))

    if 'is_profile' in kwargs and kwargs['is_profile']:

        return annotate_order(
            get_object_or_404(User, username=kwargs['username']
                              ).posts.get_queryset()
        )


def get_comments(object, post_id):
    """Функция для получения комментариев к посту без select_related"""
    comments = object.post.get_queryset().values_list('id', 'comments')
    post = Post.objects.get(pk=post_id)
    comments_filtered = []
    for posts_id, comment_id in comments:
        if posts_id == post.pk and comment_id:
            comments_filtered.append(comment_id)

    return object.objects.filter(
        id__in=comments_filtered
    ).order_by('created_at')


def get_category(object, category_slug):
    return get_object_or_404(object, slug=category_slug, is_published=True)


class PostListView(ListView):
    model = Post
    paginate_by = PAGES_LIMIT
    template_name = 'blog/index.html'

    def get_queryset(self):
        return get_posts(Post.objects, is_index=True)


class PostCreateView(LoginRequiredMixin, PostBaseMixin, CreateView):

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(UserIsPostAuthorMixin, PostBaseMixin, UpdateView):
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            args=[self.kwargs[self.pk_url_kwarg]]
        )


class PostDeleteView(UserIsPostAuthorMixin, PostBaseMixin, DeleteView):
    success_url = '/'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

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
            comments=get_comments(
                Comment,
                post_id=self.kwargs[self.pk_url_kwarg]),
            **kwargs
        )


class CategoryListView(ListView):
    model = Post
    paginate_by = PAGES_LIMIT
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            category=get_category(Category, self.kwargs[self.slug_url_kwarg]))

    def get_queryset(self):
        return get_posts(
            Post.objects,
            category_slug=self.kwargs[self.slug_url_kwarg],
            is_category=True
        )


class CommentAddView(LoginRequiredMixin, CommentMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.posts
        return super().form_valid(form)


class CommentEditView(LoginRequiredMixin, CommentMixin, UpdateView):

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            form=CreateCommentForm(instance=self.get_object()),
            post=self.posts,
            *args,
            **kwargs
        )


class CommentDeleteView(CommentMixin, DeleteView):
    pass
