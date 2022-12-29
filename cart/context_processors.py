from .views import _cart_id
from .models import Cart


def cart_items(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_count = sum([cart_item.quantity for cart_item in cart.cart_items.all()])
        # for cart_item in cart.cart_items.all():
        #     cart_count += cart_item.quantity
        return dict(cart_count=cart_count)
    except Cart.DoesNotExist:
        return dict(cart_count=0)

    
