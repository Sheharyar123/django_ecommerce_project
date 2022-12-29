from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView

from cart.views import _cart_id
from cart.models import CartItem
from .models import Category, Product

# Create your views here.


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_available=True)[:4]
        context = {"products": products}
        return render(request, "core/index.html", context)


class ProductListView(ListView):
    model = Product
    template_name = "core/product_list.html"
    context_object_name = "product_list"
    paginate_by = 2

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        query = self.request.GET.get("keyword")
        if query is not None:
            return Product.objects.filter(
                Q(name__icontains=query) | Q(category__name__icontains=query)
            )
        elif category_slug is not None:
            category = get_object_or_404(Category, slug=category_slug)
            return Product.objects.filter(is_available=True, category=category)

        return Product.objects.filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_slug"] = self.kwargs.get("category_slug")
        context["query"] = self.request.GET.get("keyword")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "core/product_detail.html"
    context_object_name = "product"

    def get_object(self):
        category_slug = self.kwargs.get("category_slug")
        product_slug = self.kwargs.get("product_slug")
        return get_object_or_404(
            Product, is_available=True, category__slug=category_slug, slug=product_slug
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["in_cart"] = CartItem.objects.filter(
            cart__cart_id=_cart_id(self.request), product=self.get_object()
        )
        return context
