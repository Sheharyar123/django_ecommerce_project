from django.contrib import admin
from .models import Category, Product

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name",
        "slug",
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "original_price",
        "discount_price",
        "stock",
        "is_available",
    )
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-updated_on", "-added_on")
    search_fields = (
        "name",
        "original_price",
    )
    list_editable = ["discount_price", "is_available"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
