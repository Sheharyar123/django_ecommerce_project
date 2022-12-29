from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from core.models import Product
from .models import Cart, CartItem

# Helper function to generate cart id
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


class CartView(View):
    def get(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        except Cart.DoesNotExist:
            cart_items = {}
        context = {"cart": cart, "cart_items": cart_items}
        return render(request, "cart/cart.html", context)


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get("product_slug"))
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            if cart_item.quantity > product.stock:
                cart_item.quantity = product.stock
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            cart_item.save()

        return redirect("cart:cart")


class RemoveSingleFromCartView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, slug=self.kwargs.get("product_slug"))
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect("cart:cart")


class RemoveItemFromCartView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, slug=self.kwargs.get("product_slug"))
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
        return redirect("cart:cart")

