# Generated by Django 3.2.9 on 2021-12-01 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20211201_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseproduct',
            name='product_detail_gcl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.gcl'),
        ),
        migrations.AlterField(
            model_name='baseproduct',
            name='product_detail_geocell',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.geocell'),
        ),
        migrations.AlterField(
            model_name='baseproduct',
            name='product_detail_geotextile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.geotextile'),
        ),
    ]