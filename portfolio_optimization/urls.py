from django.urls import path
from .views import HomePageView

urlpatterns = [
    path("portfolio-optimization/", HomePageView.as_view(), name="po-home"),
]
