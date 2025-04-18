# Generated by Django 3.2.9 on 2025-03-18 00:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_price_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='expiry',
            field=models.DateField(blank=True, default=datetime.date(2025, 4, 17), null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 3, 18, 0, 30, 19, 852262, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2025, 3, 18, 0, 30, 26, 500472, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
