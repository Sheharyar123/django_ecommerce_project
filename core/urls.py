from django.urls import path

from .views import HomePageView, ProductDetailView


app_name = "core"

urlpatterns = [
    path("", HomePageView.as_view(), name="index"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
]
