from django.urls import path
from .views import HomePageView, ChartGeneratorView, DiscountChartView, DownloadDiscount

urlpatterns = [
    path("swap_manager/", HomePageView.as_view(), name="home"),
    path(
        "generate_chart/",
        ChartGeneratorView.as_view(),
        name="generate_chart",
    ),
    path("discount_chart/", DiscountChartView.as_view(), name="discount_chart"),
    path("download_discount/", DownloadDiscount.as_view(), name="download_discount"),
]
