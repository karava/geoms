# Generated by Django 3.2.9 on 2021-12-01 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_price_expiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='GCL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('density', models.IntegerField(help_text='Unit of measure is gsm')),
                ('roll_width', models.DecimalField(decimal_places=2, help_text='Unit of measure is m', max_digits=4)),
                ('roll_length', models.DecimalField(decimal_places=2, help_text='Unit of measure is m', max_digits=5)),
                ('bentotite_specs', models.CharField(blank=True, max_length=200)),
                ('suggested_applications', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Geotextile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('density', models.IntegerField(help_text='Unit of measure is gsm')),
                ('roll_width', models.DecimalField(decimal_places=2, help_text='Unit of measure is m', max_digits=4)),
                ('roll_length', models.DecimalField(decimal_places=2, help_text='Unit of measure is m', max_digits=5)),
                ('type', models.CharField(choices=[('woven', 'Woven'), ('nonwoven', 'Non-woven')], default='woven', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='product_detail_gcl',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='products.gcl'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='product_detail_geotextile',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='products.geotextile'),
            preserve_default=False,
        ),
    ]