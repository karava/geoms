# Generated by Django 3.2.9 on 2023-12-01 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20231201_0442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseproduct',
            name='product_detail_drainage',
        ),
        migrations.RemoveField(
            model_name='baseproduct',
            name='product_detail_gcl',
        ),
        migrations.RemoveField(
            model_name='baseproduct',
            name='product_detail_geocell',
        ),
        migrations.RemoveField(
            model_name='baseproduct',
            name='product_detail_geogrid',
        ),
        migrations.RemoveField(
            model_name='baseproduct',
            name='product_detail_geotextile',
        ),
        migrations.DeleteModel(
            name='DrainageProduct',
        ),
        migrations.DeleteModel(
            name='GCL',
        ),
        migrations.DeleteModel(
            name='Geocell',
        ),
        migrations.DeleteModel(
            name='Geogrid',
        ),
        migrations.DeleteModel(
            name='Geotextile',
        ),
    ]
