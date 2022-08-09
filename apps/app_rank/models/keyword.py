from django.db import models
from django.utils import timezone


class Keyword(models.Model):
    keyword = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
