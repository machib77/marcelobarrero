from django.contrib import admin
from .models import Ticker


# Register your models here.
class TickerAdmin(admin.ModelAdmin):
    list_display = ("symbol", "company_name", "index")


admin.site.register(Ticker, TickerAdmin)
