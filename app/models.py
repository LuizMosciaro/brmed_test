from django.db import models


class CurrencyRate(models.Model):
    coin = models.CharField(max_length=255)
    dates = models.JSONField()
    rates = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)