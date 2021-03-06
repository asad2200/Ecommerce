# Generated by Django 3.2.5 on 2021-07-17 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_alter_orderitem_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'product')},
        ),
    ]
