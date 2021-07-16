from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("cart/", views.cart),
    path("category/", views.category),
    path("product/", views.product),
    path("all-products/", views.all_products),
    path("login/", views.login),
    path("register/", views.register),
]
