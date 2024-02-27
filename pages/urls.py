from django.urls import path
from .views import HomePageView, AboutPageView, ContactView, PortfolioPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("portfolio/", PortfolioPageView.as_view(), name="portfolio"),
]
