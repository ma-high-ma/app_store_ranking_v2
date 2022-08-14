from django.db import models

from apps.app_rank.constants import ScrapedHTMLStatus
from apps.app_rank.models.session import Session


class ScrapedHTML(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    page_no = models.IntegerField(default=0)
    app_handle = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, choices=ScrapedHTMLStatus.choices, default=ScrapedHTMLStatus.NOT_STARTED)
