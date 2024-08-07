from django.db import models


class BaseModel(models.Model):
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

    def __str__(self):
        try:
            if self.name:
                return self.name
            elif self.post:
                return self.post
        except AttributeError:
            return self.title
