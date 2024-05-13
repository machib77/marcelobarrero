from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    ContactView,
    PortfolioPageView,
    RobotsTxtView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("portfolio/", PortfolioPageView.as_view(), name="portfolio"),
    path("robots.txt", RobotsTxtView.as_view(content_type="text/plain"), name="robots"),
]
