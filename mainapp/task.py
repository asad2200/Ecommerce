from celery import shared_task
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def creating_order(user_id, email):
    user = User.objects.get(id=user_id)
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        order = Order.objects.create(user=user)
        total_amount = 0
        for item in cart_items:
            product = Product.objects.get(id=item.product.id)
            if product.qty >= item.qty:
                amount = item.qty*product.price
                total_amount = total_amount + amount
                OrderItem.objects.create(
                    order=order, product=product, qty=item.qty, amount=amount)
                product.qty = product.qty - item.qty
                product.save()
                item.delete()
            elif product.qty > 0:
                amount = product.qty * product.price
                total_amount = total_amount + amount
                OrderItem.objects.create(
                    order=order, product=product, qty=product.qty, amount=amount)
                item.qty = item.qty - product.qty
                item.save()
                product.qty = 0
                product.save()
        total_amount = total_amount + (total_amount * .18)
        order.amount = total_amount
        order.save()
        order = Order.objects.get(id=order.id)
        order_items = OrderItem.objects.filter(order=order)
        cart_items = CartItem.objects.filter(cart=cart)
        context = {
            'user': user,
            'order': order,
            'order_items': order_items,
            'cart_items': cart_items,
        }

        # Sending mail
        subject = 'Karma Shop - Order Confirmation'
        html_message = render_to_string(
            "mainapp/order-confirm.html", context)
        plain_message = strip_tags(html_message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, plain_message, email_from,
                  recipient_list, html_message=html_message, fail_silently=True)
        return total_amount
    except:
        subject = 'Karma Shop - Order Confirmation'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, "Some Unexpected Error occured Contact Shop Owner", email_from,
                  recipient_list)
        return None
