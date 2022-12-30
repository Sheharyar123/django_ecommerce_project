from django.urls import path
from .views import (
    CartView,
    add_to_cart,
    RemoveSingleFromCartView,
    RemoveItemFromCartView,
)

app_name = "cart"


urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("<slug:product_slug>/", add_to_cart, name="add_to_cart"),
    path(
        "remove_single/<slug:product_slug>/<int:item_id>/",
        RemoveSingleFromCartView.as_view(),
        name="remove_single_from_cart",
    ),
    path(
        "remove/<slug:product_slug>/<int:item_id>/",
        RemoveItemFromCartView.as_view(),
        name="remove_from_cart",
    ),
]
