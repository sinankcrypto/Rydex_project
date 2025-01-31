# Generated by Django 5.1.4 on 2024-12-13 20:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_categories_created_at_categories_description_and_more'),
        ('products', '0002_product_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.categories'),
        ),
    ]
