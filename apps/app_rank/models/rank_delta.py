from django.db import models

from apps.app_rank.models import ShopifyApp, Session


class RankDelta(models.Model):
    shopify_app = models.ForeignKey(ShopifyApp, on_delete=models.CASCADE)
    prev_rank = models.FloatField()
    new_rank = models.FloatField()
    rank_delta = models.FloatField(default=0.0)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    has_app_data_changed = models.BooleanField()
    extras = models.JSONField(default=dict)
    created_at = models.DateField(auto_now_add=True)
