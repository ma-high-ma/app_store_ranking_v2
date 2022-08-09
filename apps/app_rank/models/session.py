from django.db import models

from apps.app_rank.constants import SessionStatus


class Session(models.Model):
    session_id = models.CharField(max_length=250)  # String UUID
    status = models.CharField(max_length=32, choices=SessionStatus.choices, default=SessionStatus.NOT_STARTED)
    details = models.CharField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
