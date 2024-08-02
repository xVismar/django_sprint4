from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from .querysets import PostQuerySet, CategoryQuerySet
from core.models import BaseModel, TPdModel
from django.db import models
from django.utils import timezone
from django.db.models.constraints import UniqueConstraint

User = get_user_model()


class Comment(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comment_authors',
        verbose_name='Автор комментария',
    )

    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='post',
    )
    text = models.TextField(verbose_name='Текст комментария', blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания комментария',
        help_text='Время создания комментария.'
    )

    class Meta:
        verbose_name = 'комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)


class Post(TPdModel):
    text = models.TextField(verbose_name='Текст')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Автор публикации',
    )

    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='locations',
        verbose_name='Местоположение'
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories',
        verbose_name='Категория'
    )

    comments = models.ForeignKey(
        Comment,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='comments'
    )
    image = models.ImageField('Фото', upload_to='media/img', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def short_text(self):
        return truncatewords(self.text, 10)

    def get_absolute_url(self):
        return reverse('blog:profile', kwargs={'pk': self.pk})


class Category(TPdModel):
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=64,
        unique=True,
        blank=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
        ' цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('-pub_date',)


class Location(BaseModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
