# Generated by Django 3.2.9 on 2025-05-05 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_price_expiry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='alternative_names',
        ),
        migrations.RemoveField(
            model_name='product',
            name='density',
        ),
        migrations.RemoveField(
            model_name='product',
            name='fortygp_cap',
        ),
        migrations.RemoveField(
            model_name='product',
            name='fortyhc_cap',
        ),
        migrations.RemoveField(
            model_name='product',
            name='heigth',
        ),
        migrations.RemoveField(
            model_name='product',
            name='length',
        ),
        migrations.RemoveField(
            model_name='product',
            name='material',
        ),
        migrations.RemoveField(
            model_name='product',
            name='moq',
        ),
        migrations.RemoveField(
            model_name='product',
            name='packing_description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='suppliers',
        ),
        migrations.RemoveField(
            model_name='product',
            name='twentygp_cap',
        ),
        migrations.RemoveField(
            model_name='product',
            name='unit_of_measure',
        ),
        migrations.RemoveField(
            model_name='product',
            name='width',
        ),
        migrations.AlterField(
            model_name='product',
            name='long_description',
            field=models.TextField(blank=True, help_text='This is for SEO purposes, roughly 500 words'),
        ),
    ]
