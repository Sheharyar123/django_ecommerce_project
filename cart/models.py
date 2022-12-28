from django.db import models
from core.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    @property
    def get_price(self):
        if self.product.discount_price:
            return self.product.discount_price

        return self.product.original_price

    @property
    def get_subtotal(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity

        return self.product.original_price * self.quantity

    @property
    def get_tax(self):
        total = sum(self.cart.cart_items.all().get_subtotal())
        return total
