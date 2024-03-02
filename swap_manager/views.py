from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
import json

from django.http import HttpResponse
from django.views import View

# Import the Django session
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from .python_scripts import discount_usd_sofr
from .python_scripts.plotly_charts import scatter_plot


# Llamo a mi diccionario con los defaults.
curve_defaults = discount_usd_sofr.curve_defaults


class HomePageView(TemplateView):
    template_name = "swap_manager/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puse unos valores por default para que la curva se cargue desde que se abre
        context["tenors"] = curve_defaults

        context["tenors_json"] = json.dumps(context["tenors"])

        return context


class ChartGeneratorView(View):

    def post(self, request):

        rate_dict = {}

        for tenor in curve_defaults.keys():
            rate_dict[tenor] = float(request.POST.get(tenor, 0))

        # Guardar rate_dict en session
        request.session["rate_dict"] = rate_dict

        # Genero el gráfico plotly de las TASAS SPOT
        chart = scatter_plot(list(rate_dict.keys()), list(rate_dict.values()))

        return HttpResponse(chart)


class DiscountChartView(View):
    def post(self, request):
        # Recuperar rate_dict de sessions
        rate_dict = request.session.get("rate_dict", {})
        # print(rate_dict)
        disc_chart = scatter_plot(["1Y", "2Y", "3Y", "4Y"], [2, 4, 7, 9])

        return HttpResponse(disc_chart)
