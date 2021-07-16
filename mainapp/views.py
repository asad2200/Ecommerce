from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "mainapp/index.html")


def cart(request):
    return render(request, "mainapp/cart.html")


def category(request):
    return render(request, "mainapp/category.html")


def product(request):
    return render(request, "mainapp/product.html")


def all_products(request):
    return render(request, "mainapp/all-products.html")


def login(request):
    return render(request, "mainapp/login.html")


def register(request):
    return render(request, "mainapp/register.html")
