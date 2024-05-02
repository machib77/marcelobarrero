from django.shortcuts import render
from django.views.generic import TemplateView
from portfolio_optimization.models import Ticker
from django.db.models import Q


# Create your views here.
class HomePageView(TemplateView):
    template_name = "portfolio_optimization/po-home.html"


def search_ticker(request):
    search_text = request.POST.get("search")

    results = Ticker.objects.filter(
        Q(symbol__icontains=search_text)
        | Q(company_name__icontains=search_text)
        | Q(index__icontains=search_text)
    )
    context = {"results": results}
    return render(request, "partials/search-results.html", context)
