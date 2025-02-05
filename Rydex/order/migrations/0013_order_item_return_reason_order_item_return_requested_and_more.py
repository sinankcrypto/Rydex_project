# Generated by Django 5.1.4 on 2025-01-22 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_order_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_item',
            name='return_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order_item',
            name='return_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order_item',
            name='return_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]
