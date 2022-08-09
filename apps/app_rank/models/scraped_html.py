from django.db import models

from apps.app_rank.models.shopify_app import ShopifyApp
from apps.app_rank.models.session import Session


class ScrapedHTML(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    page_no = models.IntegerField(default=0)
    app_handle = models.ForeignKey(ShopifyApp, on_delete=models.CASCADE, default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

