from django.contrib import admin
from .models import (
    Profile,
    ShippingAddress,
    Brand,
    Product,
    CartItem,
    Cart,
    Order,
    OrderItem,
)

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user_id", "mobile_no1")


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "address_1",
        "country",
        "state",
        "city",
        "zipcode",
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "brand",
        "qty",
        "img",
        "price",
    )


admin.site.register(Cart)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "qty",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "total_items",
        "amount",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "qty",
        "amount",
    )
