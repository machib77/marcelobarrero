from django.db import models


# Create your models here.
class Ticker(models.Model):
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100)
    index = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol
