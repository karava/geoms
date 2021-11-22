from django.db import models
from django.db.models import base
from django.db.models.fields import CharField, BooleanField

# Choices
UNITS_OF_MEASURE = [
    ('rolls', 'Rolls'),
    ('sqm', 'SQM'),
]

# Create your models here.
class Geocell(models.Model):
    height = CharField(max_length=3)
    height.help_text = "Unit of measure is mm"
    weld_spacing = CharField(max_length=200)
    weld_spacing.help_text = "Unit of measure is mm"
    is_textured = BooleanField(default=False)

    def __str__(self):
        return ("Height: " + self.height + ", Weld spacing: " + self.weld_spacing)

class BaseProduct(models.Model):
    code = models.CharField(max_length=10, blank=True)
    material = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    suppliers = models.CharField(max_length=200, blank=True)
    suppliers.help_text = "Please comma separate names"
    unit_of_measure = models.CharField(choices=UNITS_OF_MEASURE, max_length=200, default='rolls')
    twentygp_cap = models.IntegerField(blank=True)
    fortygp_cap = models.IntegerField(blank=True, default=0)
    fortyhc_cap = models.IntegerField(blank=True, default=0)
    moq = models.IntegerField(null=True, default=0)
    alternative_names = models.CharField(max_length=200, blank=True)
    alternative_names.help_text = "Please comma separate names"
    product_detail_geocell = models.ForeignKey(Geocell, on_delete=models.CASCADE)
    our_datasheets = models.CharField(blank=True, max_length=200)    
    supplier_datasheets = models.CharField(blank=True, max_length=200)
    sample_testing_reports = models.CharField(blank=True, max_length=200)
    packing_description = models.CharField(blank=True, max_length=200)
    packing_photos = models.CharField(blank=True, max_length=200)
    images = models.CharField(blank=True, max_length=200)

