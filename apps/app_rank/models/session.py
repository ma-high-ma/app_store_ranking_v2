from django.db import models

from apps.app_rank.constants import SessionStatus


class Session(models.Model):
    session_uuid = models.CharField(max_length=250)  # String UUID
    status = models.CharField(max_length=32, choices=SessionStatus.choices, default=SessionStatus.NOT_STARTED)
    type = models.CharField(max_length=32, default='')
    details = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.session_uuid}'
