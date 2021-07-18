from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("brand-category/", views.BrandCategory.as_view(), name="brand-category"),
    path("item-category/", views.ItemCategory.as_view(), name="item-category"),
    path("all-products/", views.AllProducts.as_view(), name="all-products"),
    path("search/", views.AllProducts.as_view(), name="search"),
    path("product/<int:id>", views.ProductView.as_view(), name="product"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile-view/", views.ProfileView.as_view(), name="profile-view"),
    path("profile-edit/", views.ProfileEdit.as_view(), name="profile-edit"),
    path("cart-view/", views.cart_view, name="cart-view"),
    path("cart-add/<int:id>", views.CartAdd.as_view(), name="cart-add"),
    path("checkout/", views.checkout, name="checkout"),
]
