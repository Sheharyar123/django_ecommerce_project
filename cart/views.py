from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from core.models import Product, Variation
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
            cart = None
        context = {"cart": cart, "cart_items": cart_items}
        return render(request, "cart/cart.html", context)


def add_to_cart(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    product_variation = []
    for item in request.POST:
        key = item
        value = request.POST.get(key)
        try:
            variation = Variation.objects.get(
                product=product, category__iexact=key, value__iexact=value
            )
            product_variation.append(variation)
        except:
            pass
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if len(product_variation) > 0:
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.quantity += 1
        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        if len(product_variation) > 0:
            for item in product_variation:
                cart_item.variations.add(item)
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
