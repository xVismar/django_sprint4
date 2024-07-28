from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatewords

from .querysets import PostQuerySet, CategoryQuerySet
from core.models import BaseModel, TPdModel
from django.db import models


User = get_user_model()


class Post(TPdModel):
    text = models.TextField(verbose_name='Текст')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Автор публикации'

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

    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def short_text(self):
        return truncatewords(self.text, 10)

    @classmethod
    def posts(cls):
        return cls.objects.filter(category__is_published=True).check_pub_time()


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

    objects = CategoryQuerySet.as_manager()

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


class Commentary(BaseModel):
    pass
