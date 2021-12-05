from django.db import models
from django.db.models import base
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, BooleanField, DecimalField, IntegerField

# Choices
UNITS_OF_MEASURE = [
    ('rolls', 'Rolls'),
    ('sqm', 'SQM'),
]

INCOTERMS = [
    ('fob', 'FOB'),
    ('cif', 'CIF'),
    ('ddp', 'DDP'),
]

CURRENCIES = [
    ('usd', 'USD'),
    ('aud', 'AUD'),
]

PRICE_TYPES = [
    ('sale', 'Sale'),
    ('cost', 'Cost'),
    ('rrp', 'RRP'),
]

GEOTEXTILE_TYPES = [
    ('woven', 'Woven'),
    ('nonwoven', 'Non-woven'),
]

GEOGRID_TYPES = [
    ('BI', 'BIAXIAL'),
    ('TRI', 'TRIAXIAL'),
]

DRAINAGE_TYPES = [
    ('strip', 'Strip Drain'),
    ('sheet', 'Sheet Drain'),
]

# Create your models here.
class Geocell(models.Model):
    height = models.IntegerField()
    height.help_text = "Unit of measure is mm"
    weld_spacing = models.IntegerField()
    weld_spacing.help_text = "Unit of measure is mm"
    is_textured = BooleanField(default=False)

    def __str__(self):
        return ("Height: " + str(self.height) + ", Weld spacing: " + str(self.weld_spacing))

class GCL(models.Model):
    density = models.IntegerField()
    density.help_text = "Unit of measure is gsm"
    roll_width = DecimalField(max_digits=4, decimal_places=2)
    roll_width.help_text = "Unit of measure is m"
    roll_length = DecimalField(max_digits=5, decimal_places=2)
    roll_length.help_text = "Unit of measure is m"
    bentotite_specs = models.CharField(max_length=200, blank=True)
    suggested_applications = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return ("Density: " + str(self.density) + ", Roll width: " + str(self.roll_width))

class Geotextile(models.Model):
    density = models.IntegerField()
    density.help_text = "Unit of measure is gsm"
    roll_width = DecimalField(max_digits=4, decimal_places=2)
    roll_width.help_text = "Unit of measure is m"
    roll_length = DecimalField(max_digits=5, decimal_places=2)
    roll_length.help_text = "Unit of measure is m"
    type = models.CharField(choices=GEOTEXTILE_TYPES, max_length=200, default='woven')
    # aperture_size do we need this?

    def __str__(self):
        return ("Density: " + str(self.density) + ", Type: " + self.type)
class Geogrid(models.Model):
    shape = models.CharField(choices=GEOGRID_TYPES, max_length=200) 
    strength_md = models.IntegerField()
    strength_md.help_text = "Strength in machine direction in kN"
    strength_td = models.IntegerField()
    strength_td.help_text = "Strength in transverse direction in kN"

    def __str__(self):
        return ("Shape: " + self.shape + ", Strength: " + str(self.strength_md) + "x" + str(self.strength_td))

class DrainageProduct(models.Model):
    type = models.CharField(choices=DRAINAGE_TYPES, max_length=200, default='strip')
    type.help_text = "FreDrain = Strip Drain, TerraDrain = Sheet Drain"
    height = models.IntegerField()
    height.help_text = "Unit of measure is mm"
    roll_width = models.IntegerField()
    roll_width.help_text = "Unit of measure is mm"
    double_cuspated = BooleanField(default=False)

    def __str__(self):
        return("Type: " + self.type + ", Height: " + str(self.height) + "x" + str(self.roll_width))

class BaseProduct(models.Model):
    code = models.CharField(max_length=10, blank=True)
    material = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    suppliers = models.CharField(max_length=200, blank=True)
    suppliers.help_text = "Please comma separate names"
    unit_of_measure = models.CharField(choices=UNITS_OF_MEASURE, max_length=200, default='rolls')
    twentygp_cap = models.IntegerField(blank=True, null=True, default=0)
    fortygp_cap = models.IntegerField(blank=True, null=True, default=0)
    fortyhc_cap = models.IntegerField(blank=True, null=True, default=0)
    moq = models.IntegerField(null=True, default=0)
    alternative_names = models.CharField(max_length=200, blank=True)
    alternative_names.help_text = "Please comma separate names"
    packing_description = models.CharField(blank=True, max_length=200)
    product_detail_geocell = models.OneToOneField(Geocell, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    product_detail_geotextile = models.OneToOneField(Geotextile, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    product_detail_gcl = models.OneToOneField(GCL, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    product_detail_geogrid = models.OneToOneField(Geogrid, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    product_detail_drainage = models.OneToOneField(DrainageProduct, on_delete=models.CASCADE, null=True, blank=True, editable=False)

class Price(models.Model):
    type = models.CharField(choices=PRICE_TYPES, max_length=200, default='sale')
    date = models.DateField()
    qty = models.IntegerField
    unit_of_measure = models.CharField(choices=UNITS_OF_MEASURE, max_length=200, default='rolls')
    incoterm = models.CharField(choices=INCOTERMS, max_length=200, default='cif')
    currency = models.CharField(choices=CURRENCIES, max_length=200, default='usd')
    expiry = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    base_product = models.ForeignKey(BaseProduct, on_delete=CASCADE, related_name='price')


# File models
class DatasheetFile(models.Model):
    file = models.FileField(upload_to="products/datasheets/")
    datasheet = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='datasheets')
class TestingFile(models.Model):
    file = models.FileField(upload_to="products/testing_reports/")
    datasheet = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='testReports')
class ImageFile(models.Model):
    file = models.ImageField(upload_to="products/product_images/")
    image = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='images')

