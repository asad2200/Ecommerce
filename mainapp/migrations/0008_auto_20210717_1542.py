# Generated by Django 3.2.5 on 2021-07-17 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_rename_address_profile_shipping_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='cart_id',
            new_name='cart',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='product_id',
            new_name='product',
        ),
    ]
