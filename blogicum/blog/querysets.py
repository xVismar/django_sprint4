from django.db import models


class PostQuerySet(models.QuerySet):

    def get_object(self):
        return self.get_object().prefetch_related(
            'category',
            'author',
            'location'
        )
