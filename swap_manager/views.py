from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
import json

from django.http import HttpResponse
from django.views import View

# Import the Django session
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from .python_scripts.usd_sofr import curve_defaults, discount_usd_sofr
from .python_scripts.plotly_charts import scatter_plot

from io import BytesIO
import pandas as pd

# Llamo a mi diccionario con los defaults.
curve_defaults = curve_defaults


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

        # Ejecuto la función que calcula los fd
        df_usd = discount_usd_sofr(rate_dict)

        # Guardo el dataframe df_usd en session
        df_usd_str = df_usd.copy().reset_index()
        df_usd_str["date"] = df_usd_str["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        df_usd_dict = df_usd_str.to_dict(orient="records")
        request.session["df_usd_dict"] = df_usd_dict

        # Genero el gráfico
        disc_chart = scatter_plot(list(df_usd.date), list(df_usd.df))

        return HttpResponse(disc_chart)


class DownloadDiscount(View):
    def post(self, request):
        # Recupero el dataframe df_usd de sessions
        df_usd_dict = request.session.get("df_usd_dict", {})
        df_usd = pd.DataFrame(df_usd_dict)

        # Guardo el archivo excel como bytes  en memoria
        excel_buffer = BytesIO()
        excel_writer = pd.ExcelWriter(excel_buffer, engine="xlsxwriter")  # type:ignore
        df_usd.to_excel(excel_writer, index=False)
        excel_writer.close()

        # Creo una respuesta con el archivo excel
        response = HttpResponse(
            excel_buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="dataframe.xlsx"'
        return response
