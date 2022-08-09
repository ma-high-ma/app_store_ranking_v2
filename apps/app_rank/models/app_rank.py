from django.db import models

from apps.app_rank.models.keyword import Keyword
from apps.app_rank.models.session import Session
from apps.app_rank.models.shopify_app import ShopifyApp


class AppRank(models.Model):
    shopify_app = models.ForeignKey(ShopifyApp, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    rank = models.FloatField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
