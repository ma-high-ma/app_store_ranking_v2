from django.db import models


class ErrorLog(models.Model):
    error_message = models.CharField(max_length=1000)
    session_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
