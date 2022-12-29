from django.contrib import admin
from .models import Category, Product, Variation

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
    ordering = ("-modified_on", "-added_on")
    search_fields = (
        "name",
        "original_price",
    )
    list_editable = ["discount_price", "is_available"]


class VariationAdmin(admin.ModelAdmin):
    list_display = ["value", "category", "is_active"]
    list_editable = [
        "is_active",
    ]
    ordering = ("-modified_on", "-added_on")
    search_fields = ("name",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
