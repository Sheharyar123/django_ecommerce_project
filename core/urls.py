from django.urls import path

from .views import HomePageView, ProductListView, ProductDetailView


app_name = "core"

urlpatterns = [
    path("", HomePageView.as_view(), name="index"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path(
        "products/<slug:category_slug>/",
        ProductListView.as_view(),
        name="product_list_by_category",
    ),
    path(
        "product/<slug:category_slug>/<slug:product_slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
]
