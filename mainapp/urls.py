from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("category/", views.Category.as_view(), name="category"),
    path("cart/", views.cart),
    path("product/", views.product),
    path("all-products/", views.all_products),
    path("login/", views.login),
    path("register/", views.register),
]
