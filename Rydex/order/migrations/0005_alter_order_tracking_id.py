# Generated by Django 5.1.4 on 2024-12-28 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_tracking_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=8, unique=True),
        ),
    ]