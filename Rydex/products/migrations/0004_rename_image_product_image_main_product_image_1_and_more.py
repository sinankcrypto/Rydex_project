# Generated by Django 5.1.4 on 2024-12-16 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='image_main',
        ),
        migrations.AddField(
            model_name='product',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]
