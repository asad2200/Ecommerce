from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField

# Create your models here.
class Profile(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    mobile_no1 = models.CharField(max_length=14, unique=True)
    mobile_no2 = models.CharField(max_length=14, unique=True, blank=True, null=True)
    address = models.ManyToManyField(to="ShippingAddress", blank=True)

    def __str__(self):
        return str(self.user_id)


class ShippingAddress(models.Model):
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=30)
    address_1 = models.CharField(max_length=51, default="")
    address_2 = models.CharField(max_length=51, blank=True, null=True)

    def __str__(self):
        return self.address_1


class Brand(models.Model):
    name = models.CharField(max_length=51)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=51)
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE)
    qty = models.IntegerField()
    img = models.ImageField(upload_to="products/")
    description = models.TextField()
    price = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.name


class Cart(models.Model):
    user_id = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user_id)


class CartItem(models.Model):
    class Meta:
        unique_together = (("cart_id", "product_id"),)

    cart_id = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def __str__(self) -> str:
        return str(self.cart_id) + " " + str(self.product_id)


class Order(models.Model):
    user_id = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, blank=True
    )
    total_items = models.IntegerField()
    amount = models.FloatField()

    def __str__(self) -> str:
        return str(self.user_id)


class OrderItem(models.Model):
    class Meta:
        unique_together = (("order_id", "product_id"),)

    order_id = models.ForeignKey(to="Order", on_delete=models.CASCADE)
    product_id = models.ForeignKey(
        to="Product", on_delete=models.SET_NULL, null=True, blank=True
    )
    qty = models.IntegerField()
    amount = models.FloatField()

    def __str__(self) -> str:
        return str(self.cart_id) + " " + str(self.product_id)
