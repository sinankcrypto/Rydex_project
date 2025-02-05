# Generated by Django 5.1.4 on 2025-01-16 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='min_order_amount',
            field=models.DecimalField(decimal_places=2, help_text='minimum order value to apply the coupon', max_digits=6),
        ),
    ]
