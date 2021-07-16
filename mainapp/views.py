from django.http import request
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Product, Brand


# Create your views here.
class Index(TemplateView):
    template_name = "mainapp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.order_by("-qty")[:20]
        context["products"] = products
        return context


class Category(ListView):
    model = Brand

    def get_context_data(self, *args, **kwargs):
        queryset = kwargs.pop("object_list", None)
        if queryset is None:
            self.object_list = self.get_queryset(*args, **kwargs)
        return super().get_context_data(**kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(Category, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("name")
        context = []
        for q in qs:
            total_brand_items = q.product_set.all().count()
            context.append(
                {
                    "brand": q,
                    "products": total_brand_items,
                }
            )
        return context

    def post(self, request, *args, **kwargs):
        brand_id = request.POST.get("brand_id")
        products = Product.objects.filter(brand_id=brand_id)
        context = self.get_context_data(*args, **kwargs)
        context["products"] = products
        return self.render_to_response(context)

    template_name = "mainapp/category.html"


def cart(request):
    return render(request, "mainapp/cart.html")


def product(request):
    return render(request, "mainapp/product.html")


def all_products(request):
    return render(request, "mainapp/all-products.html")


def login(request):
    return render(request, "mainapp/login.html")


def register(request):
    return render(request, "mainapp/register.html")
