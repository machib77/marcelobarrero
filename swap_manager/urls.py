from django.urls import path
from .views import HomePageView

urlpatterns = [
    path("swap_manager/", HomePageView.as_view(), name="home"),
]
