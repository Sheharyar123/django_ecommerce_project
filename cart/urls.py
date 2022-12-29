from django.urls import path
from .views import CartView, AddToCartView, RemoveSingleFromCartView, RemoveItemFromCartView

app_name = "cart"


urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("<slug:product_slug>/", AddToCartView.as_view(), name="add_to_cart"),
    path("remove_single/<slug:product_slug>/", RemoveSingleFromCartView.as_view(), name="remove_single_from_cart"),
    path("remove/<slug:product_slug>/", RemoveItemFromCartView.as_view(), name="remove_from_cart"),
]
