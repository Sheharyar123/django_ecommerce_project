from django.db import models
from core.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    @property
    def get_total(self):
        cart_items = self.cart_items.all()
        total = 0
        for cart_item in cart_items:
            total += cart_item.get_subtotal
        return total

    @property
    def get_tax(self):
        return round((5 * self.get_total) / 100, 2)

    @property
    def get_total_with_tax(self):
        return round(self.get_total + self.get_tax, 2)


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

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
