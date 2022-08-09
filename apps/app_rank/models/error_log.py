from django.db import models

from apps.app_rank.models import Session


class ErrorLog(models.Model):
    error_message = models.CharField(max_length=500)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, default='')
    created_at = models.DateField(auto_now_add=True)
