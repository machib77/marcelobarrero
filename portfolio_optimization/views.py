from django.shortcuts import render
from django.views.generic import TemplateView
from portfolio_optimization.models import Ticker, SelectedTicker, DateRange
from django.db.models import Q
import json
from django.http import HttpResponse
from portfolio_optimization.optimize import optimize_portfolio


# Create your views here.
class HomePageView(TemplateView):
    template_name = "portfolio_optimization/po-home.html"

    def get(self, request, *args, **kwargs):
        request.session.create()
        return super().get(request, *args, **kwargs)


def search_ticker(request):
    search_text = request.POST.get("search")

    results = Ticker.objects.filter(
        Q(symbol__icontains=search_text)
        | Q(company_name__icontains=search_text)
        | Q(index__icontains=search_text)
    )
    context = {"results": results}
    return render(request, "partials/search-results.html", context)


def add_ticker(request):
    if request.method == "GET":
        ticker_id = request.GET.get("ticker_id")
        ticker = Ticker.objects.get(id=ticker_id)
        session_key = request.session.session_key
        selected_ticker, created = SelectedTicker.objects.get_or_create(
            ticker=ticker, session_key=session_key
        )
        selected_tickers = SelectedTicker.objects.filter(session_key=session_key)
        context = {"selected_tickers": selected_tickers}
        return render(request, "partials/selected_tickers.html", context)  # type: ignore


def update_date_range(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        session_key = request.session.session_key

        date_range, created = DateRange.objects.update_or_create(
            session_key=session_key,
            defaults={"start_date": start_date, "end_date": end_date},
        )

        return HttpResponse(status=200)


def run_calculations(request):
    if request.method == "POST":
        session_key = request.session.session_key
        selected_tickers = SelectedTicker.objects.filter(session_key=session_key)
        date_range = DateRange.objects.get(session_key=session_key)
        date_list = date_range.get_dates_list()
        ticker_symbols = [ticker.ticker.symbol for ticker in selected_tickers]
        print(date_list)
        print(ticker_symbols)
        corr_matrix, efficient_frontier = optimize_portfolio(ticker_symbols, date_list)

        context = {
            "ticker_symbols": ticker_symbols,
            "corr_matrix_html": corr_matrix,
            "efficient_frontier": efficient_frontier,
        }
        return render(request, "partials/calculation-results.html", context)
