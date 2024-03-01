from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class HomePageView(TemplateView):
    template_name = "swap_manager/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenors"] = [
            "1D",
            "1W",
            "2W",
            "3W",
            "1M",
            "2M",
            "3M",
            "4M",
            "5M",
            "6M",
            "7M",
            "8M",
            "9M",
            "10M",
            "11M",
            "1Y",
            "1.5Y",
            "2Y",
            "3Y",
            "4Y",
            "5Y",
            "6Y",
            "7Y",
            "8Y",
            "9Y",
            "10Y",
            "12Y",
            "15Y",
            "20Y",
        ]
        return context
