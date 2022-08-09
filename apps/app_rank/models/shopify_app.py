from django.db import models


class ShopifyApp(models.Model):
    app_handle = models.CharField(max_length=1000, primary_key=True)
    name = models.CharField(default='', max_length=500)
    developed_by = models.CharField(default='', max_length=500)
    created_at = models.DateField(auto_now_add=True)
