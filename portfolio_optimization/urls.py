from django.urls import path
from .views import HomePageView
from . import views

urlpatterns = [
    path("portfolio-optimization/", HomePageView.as_view(), name="po-home"),
]

htmx_urlpatterns = [path("search-ticker/", views.search_ticker, name="search-ticker")]

urlpatterns += htmx_urlpatterns
