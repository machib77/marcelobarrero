from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
import json

from django.http import HttpResponse
from django.views import View

# Import the Django session
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from .python_scripts.usd_sofr import curve_defaults, swap_defaults, discount_usd_sofr
from .python_scripts.plotly_charts import scatter_plot

from io import BytesIO
import pandas as pd

from .python_scripts.swap_valuation import fix_leg_valuation, float_leg_valuation

# Llamo a mi diccionario con los defaults.
curve_defaults = curve_defaults
swap_defaults = swap_defaults


class HomePageView(TemplateView):
    template_name = "swap_manager/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puse unos valores por default para que la curva se cargue desde que se abre
        context["curve_defaults"] = curve_defaults
        context["swap_defaults"] = swap_defaults

        context["curve_defaults_json"] = json.dumps(context["curve_defaults"])
        context["swap_defaults_json"] = json.dumps(context["swap_defaults"])

        return context


class ChartGeneratorView(View):

    def post(self, request):

        rate_dict = {}
        swap_inputs = {}

        for tenor in curve_defaults.keys():
            rate_dict[tenor] = float(request.POST.get(tenor, 0))

        for swap_default in swap_defaults.keys():
            swap_inputs[swap_default] = float(request.POST.get(swap_default, 0))

        # Guardar rate_dict en session
        request.session["rate_dict"] = rate_dict
        request.session["swap_inputs"] = swap_inputs

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


class GenerateFixView(View):
    def post(self, request, *args, **kwargs):

        # Recupero el swap inputs de session
        swap_inputs = request.session.get("swap_inputs", {})

        notional = swap_inputs["notional"]
        fix_rate = swap_inputs["fix-rate"]
        flow_years = int(swap_inputs["flow-years"])

        # Recupero el dataframe df_usd de sessions
        df_usd_dict = request.session.get("df_usd_dict", {})
        df_usd = pd.DataFrame(df_usd_dict)

        df = fix_leg_valuation(notional, fix_rate / 100, flow_years, df_usd)

        # Guardo fix_leg en session
        df_str = df.copy()
        df_str["start_date"] = df_str["start_date"].apply(
            lambda x: x.strftime("%Y-%m-%d")
        )
        df_str["end_date"] = df_str["end_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        df_dict = df_str.to_dict(orient="records")
        request.session["fix_leg_dict"] = df_dict

        # Guardo fix_leg pv en session
        pv = df.pv.sum()
        request.session["fix_leg_pv"] = pv

        df_html = df.to_html()
        return HttpResponse(df_html)


class GenerateFloatView(View):
    def post(self, request):

        # Recupero fix-leg de session
        fix_leg_dict = request.session.get("fix_leg_dict", {})
        fix_leg = pd.DataFrame(fix_leg_dict)[
            [
                "dtm",
                "start_date",
                "end_date",
                "btw_days",
                "notional",
                "amortization",
                "df",
            ]
        ].copy()

        float_leg = float_leg_valuation(fix_leg)

        # Guardo float_leg pv en session
        pv = float_leg.pv.sum()
        request.session["float_leg_pv"] = pv

        return HttpResponse(float_leg.to_html())


class FixPresentValueView(View):
    def post(self, request):
        # Recupero fix_leg pv de session
        fix_leg_pv = request.session.get("fix_leg_pv", {})
        return HttpResponse(fix_leg_pv)


class FloatPresentValueView(View):
    def post(self, request):
        # Recupero float_leg pv de session
        float_leg_pv = request.session.get("float_leg_pv", {})
        return HttpResponse(float_leg_pv)


class MarkToMarketView(View):
    def post(self, request):
        # Recupero fix_leg pv y float_leg pv de session
        fix_leg_pv = request.session.get("fix_leg_pv", {})
        float_leg_pv = request.session.get("float_leg_pv", {})
        mtm = fix_leg_pv + float_leg_pv
        return HttpResponse(mtm)
