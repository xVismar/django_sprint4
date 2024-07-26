from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Базовая абстрактная модель."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
        help_text='Время создания записи.'
    )

    class Meta:
        abstract = True
        verbose_name = 'Базовая модель'


class TPdModel(BaseModel):
    """Title Pub_date абстрактная модель, дополняет BaseModel."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )

    pub_date = models.DateTimeField(
        auto_now=False,
        default=timezone.now,
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно делать'
        ' отложенные публикации.'
    )

    class Meta:
        abstract = True
        verbose_name = 'tpd модель'

    def __str__(self):
        return self.title

    @classmethod
    def posts(cls):
        return cls.objects.filter(category__is_published=True).check_time()
