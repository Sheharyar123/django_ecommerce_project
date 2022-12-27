from django.shortcuts import render
from django.views.generic import View, DetailView

from .models import Product

# Create your views here.


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all().filter(is_available=True)[:4]
        context = {"products": products}
        return render(request, "core/index.html", context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "core/product_detail.html"
    context_object_name = "product"
