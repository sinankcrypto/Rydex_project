# Generated by Django 5.1.4 on 2024-12-28 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=8, unique=True),
        ),
    ]
