from django.urls import path
from .views import (
    HomePageView,
    ChartGeneratorView,
    DiscountChartView,
    DownloadDiscount,
    GenerateSwapView,
    GenerateFloatView,
)

urlpatterns = [
    path("swap-manager/", HomePageView.as_view(), name="home"),
    path(
        "generate-chart/",
        ChartGeneratorView.as_view(),
        name="generate_chart",
    ),
    path("discount-chart/", DiscountChartView.as_view(), name="discount_chart"),
    path("download-discount/", DownloadDiscount.as_view(), name="download_discount"),
    path("generate-swap/", GenerateSwapView.as_view(), name="generate_swap"),
    path("generate-float/", GenerateFloatView.as_view(), name="generate_float"),
]
