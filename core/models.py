from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    name = models.CharField("Category Name", max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = RichTextField(blank=True)
    image = models.ImageField(
        "Category Image", upload_to="photos/categories", blank=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "core:product_list_by_category", kwargs={"category_slug": self.slug}
        )


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField("Product Name", max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    image = models.ImageField("Product Image", upload_to="photos/products")
    description = RichTextField(blank=True)
    stock = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "core:product_detail",
            kwargs={"category_slug": self.category.slug, "product_slug": self.slug},
        )


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(category="color", is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(category="size", is_active=True)


class Variation(models.Model):
    VARIATION_CATEGORY = (("color", "color"), ("size", "size"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=VARIATION_CATEGORY)
    value = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    # Manager
    objects = VariationManager()

    def __str__(self):
        return self.value
