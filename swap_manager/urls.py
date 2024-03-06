from django.urls import path
from .views import (
    HomePageView,
    ChartGeneratorView,
    DiscountChartView,
    DownloadDiscount,
    GenerateFixView,
    GenerateFloatView,
    FixPresentValueView,
    FloatPresentValueView,
    MarkToMarketView,
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
    path("generate-fix/", GenerateFixView.as_view(), name="generate_fix"),
    path("generate-float/", GenerateFloatView.as_view(), name="generate_float"),
    path("fix-present-value/", FixPresentValueView.as_view(), name="fix_pv"),
    path("float-present-value/", FloatPresentValueView.as_view(), name="float_pv"),
    path("mtm/", MarkToMarketView.as_view(), name="mtm"),
]
