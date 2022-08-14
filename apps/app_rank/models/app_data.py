from django.db import models

from apps.app_rank.models.shopify_app import ShopifyApp


class AppData(models.Model):
    shopify_app = models.ForeignKey(ShopifyApp, on_delete=models.CASCADE)
    reviews_rating = models.FloatField(default=0.0)
    reviews_count = models.IntegerField(default=0)
    signifiers = models.JSONField(default=dict)
    categories = models.JSONField(default=list)
    pricing = models.JSONField(default=dict)
    extras = models.JSONField(default=dict)
    hash = models.CharField(max_length=50, null=True)
    created_at = models.DateField(auto_now_add=True)
