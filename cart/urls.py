from django.urls import path
from .views import CartView, AddToCartView

app_name = "cart"


urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("<slug:product_slug>/", AddToCartView.as_view(), name="add_to_cart"),
]
