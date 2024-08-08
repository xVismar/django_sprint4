from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from django.utils import timezone

from .querysets import PostQuerySet

User = get_user_model()


class PublishedModel(models.Model):
    """Базовая абстрактная модель."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию или категорию.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
        help_text='Время создания записи.'
    )

    class Meta:
        abstract = True
        verbose_name = 'Базовая модель'


class Category(PublishedModel):

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )

    description = models.TextField(verbose_name='Описание')

    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
                  ' цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Comment(PublishedModel):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comments',
        verbose_name='Автор комментария',
    )

    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )

    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)


class Post(PublishedModel):

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )

    text = models.TextField(verbose_name='Текст')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_posts',
        verbose_name='Автор публикации',
    )

    pub_date = models.DateTimeField(
        auto_now=False,
        default=timezone.now,
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно делать'
                  ' отложенные публикации.'
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name='location_posts',
        verbose_name='Местоположение'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories_posts',
        verbose_name='Категория'
    )

    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='blog/',
        verbose_name='Изображение'
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def short_text(self):
        """Метод для модели поста, чтобы 'обрезать' текст поста в админке"""
        return truncatewords(self.text, 10)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=self.pk)

    def __str__(self):
        return self.title
