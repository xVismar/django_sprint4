from django.db import models
from django.utils import timezone


class CategoryQuerySet(models.query.QuerySet):

    def published(self):
        return self.filter(is_published=True)


class PostQuerySet(CategoryQuerySet):

    def check_pub_time(self):
        return self.filter(pub_date__lte=timezone.now()).published()
