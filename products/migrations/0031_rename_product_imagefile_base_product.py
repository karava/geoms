# Generated by Django 3.2.9 on 2023-09-28 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0030_auto_20230928_0201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagefile',
            old_name='product',
            new_name='base_product',
        ),
    ]