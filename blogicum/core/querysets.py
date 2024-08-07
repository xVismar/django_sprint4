from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):

    def published_before_now(self):
        return self.filter(is_published=True, pub_date__lte=timezone.now())

    def published_in_published_category(self):
        return self.select_related('category').published_before_now().filter(
            category__is_published=True
        )
