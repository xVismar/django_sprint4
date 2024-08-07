from django.db import models
from django.utils import timezone


class PostManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().select_related(
            'category',
            'location',
            'author').filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
        ).order_by('-pub_date')
        )

    class Meta:
        abstract = True
