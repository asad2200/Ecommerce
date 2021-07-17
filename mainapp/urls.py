from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("category/", views.Category.as_view(), name="category"),
    path("all-products/", views.AllProducts.as_view(), name="all-products"),
    path("search/", views.AllProducts.as_view(), name="search"),
    path("cart/", views.cart),
    path("product/", views.product),
    path("login/", views.login),
    path("register/", views.register),
]
