from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
import json

# Create your views here.


class HomePageView(TemplateView):
    template_name = "swap_manager/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puse unos valores por default para que la curva se cargue desde que se abre
        context["tenors"] = {
            "1D": 5.31,
            "1W": 5.3225,
            "2W": 5.3270,
            "3W": 5.3367,
            "1M": 5.3475,
            "2M": 5.3639,
            "3M": 5.3770,
            "4M": 5.3796,
            "5M": 5.3707,
            "6M": 5.3479,
            "7M": 5.3168,
            "8M": 5.2880,
            "9M": 5.2523,
            "10M": 5.2153,
            "11M": 5.1767,
            "1Y": 5.1350,
            "1.5Y": 4.7983,
            "2Y": 4.5490,
            "3Y": 4.2404,
            "4Y": 4.0897,
            "5Y": 4.0165,
            "6Y": 3.9823,
            "7Y": 3.9654,
            "8Y": 3.9602,
            "9Y": 3.9633,
            "10Y": 3.9694,
            "12Y": 3.9886,
            "15Y": 4.0121,
            "20Y": 3.9894,
        }

        context["tenors_json"] = json.dumps(context["tenors"])

        return context
