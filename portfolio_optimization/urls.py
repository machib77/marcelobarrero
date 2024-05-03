from django.urls import path
from .views import HomePageView, add_ticker
from . import views

urlpatterns = [
    path("portfolio-optimization/", HomePageView.as_view(), name="po-home"),
]

htmx_urlpatterns = [
    path("search-ticker/", views.search_ticker, name="search-ticker"),
    path("add-ticker/", views.add_ticker, name="add-ticker"),  # type: ignore
    path("run-calculations", views.run_calculations, name="run-calculations"),  # type: ignore
]

urlpatterns += htmx_urlpatterns
