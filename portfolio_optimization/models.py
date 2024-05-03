from django.db import models


# Create your models here.
class Ticker(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100)
    index = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol


class SelectedTicker(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.ticker.symbol
