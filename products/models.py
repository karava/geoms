from django.db import models
from django.db.models import base
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, BooleanField, DecimalField, IntegerField
from datetime import date, timedelta
from django.contrib.contenttypes.fields import GenericRelation
from knowledge_base.models import Media
from storage_backends import PublicMediaStorage

# Functions
def get_expiry_date():
    return date.today() + timedelta(days=30)

# Choices
UNITS_OF_MEASURE = [
    ('rolls', 'Rolls'),
    ('sqm', 'SQM'),
]

CURRENCIES = [
    ('usd', 'USD'),
    ('aud', 'AUD'),
]

CATEGORIES = [
    ('geocell', 'Geocell'),
    ('geotextile', 'Geotextile'),
    ('gcl', 'GCL'),
    ('geogrid', 'Geogrid'),
    ('drainage', 'Drainage'),
]

SUB_CATEGORIES = [
    ('strip', 'Drainage - Strip Drain'),
    ('sheet', 'Drainage - Sheet Drain'),
    ('powder', 'GCL - Powder'),
    ('granules', 'GCL - Granules'),
    ('biaxial', 'Geogrid - Biaxial'),
    ('triaxial', 'Geogrid - Triaxial'),
    ('composite', 'Geogrid - Composite Biaxial'),
    ('woven', 'Geotextiel - Woven'),
    ('nonwoven', 'Geotextile - Non-woven'),
]

DRAINAGE_SUB_CATEGORIES = [
    ('strip', 'Strip Drain'),
    ('sheet', 'Sheet Drain'),
]

GCL_SUB_CATEGORIES = [
    ('powder', 'Powder'),
    ('granules', 'Granules')
]

GEOGRID_SUB_CATEGORIES = [
    ('BI', 'BIAXIAL'),
    ('TRI', 'TRIAXIAL'),
]

GEOTEXTILE_SUB_CATEGORIES = [
    ('woven', 'Woven'),
    ('nonwoven', 'Non-woven'),
]

RESOURCE_TYPES = [
    ('product_image', 'Product Image'),
    ('datasheet', 'Datasheet'),
    ('brochure', 'Brochure'),
    ('installation_guide', 'Installation Guide'),
    ('accessory_guide', 'Accessory Guide'),
    ('test_report', 'Test Report'),
]

# Create your models here.
class Application(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Geocell(models.Model):
    height = models.IntegerField()
    height.help_text = "Unit of measure is mm"
    weld_spacing = models.IntegerField()
    weld_spacing.help_text = "Unit of measure is mm"
    is_textured = BooleanField(default=False)

    def __str__(self):
        return("Code: " + str(self.baseproduct.code))

class GCL(models.Model):
    density = models.IntegerField()
    density.help_text = "Unit of measure is gsm"
    roll_width = DecimalField(max_digits=4, decimal_places=2)
    roll_width.help_text = "Unit of measure is m"
    roll_length = DecimalField(max_digits=5, decimal_places=2)
    roll_length.help_text = "Unit of measure is m"
    bentonite_specs = models.CharField(max_length=200, blank=True)
    sub_category = models.CharField(choices=GCL_SUB_CATEGORIES, max_length=200)

    def __str__(self):
        return("Code: " + str(self.baseproduct.code))

class Geotextile(models.Model):
    density = models.IntegerField()
    density.help_text = "Unit of measure is gsm"
    roll_width = DecimalField(max_digits=4, decimal_places=2)
    roll_width.help_text = "Unit of measure is m"
    roll_length = DecimalField(max_digits=5, decimal_places=2)
    roll_length.help_text = "Unit of measure is m"
    sub_category = models.CharField(choices=GEOTEXTILE_SUB_CATEGORIES, max_length=200)
    # aperture_size do we need this?

    def __str__(self):
        return("Code: " + str(self.baseproduct.code))
class Geogrid(models.Model):
    sub_category = models.CharField(choices=GEOGRID_SUB_CATEGORIES, max_length=200) 
    strength_md = models.IntegerField()
    strength_md.help_text = "Strength in machine direction in kN"
    strength_td = models.IntegerField()
    strength_td.help_text = "Strength in transverse direction in kN"

    def __str__(self):
        return("Code: " + str(self.baseproduct.code))

class DrainageProduct(models.Model):
    sub_category = models.CharField(choices=DRAINAGE_SUB_CATEGORIES, max_length=200)
    height = models.IntegerField()
    height.help_text = "Unit of measure is mm"
    roll_width = models.IntegerField()
    roll_width.help_text = "Unit of measure is mm"
    double_cuspated = BooleanField(default=False)

    def __str__(self):
        return("Code: " + str(self.baseproduct.code))

class BaseProduct(models.Model):
    category = models.CharField(choices=CATEGORIES, max_length=200, blank=True)
    sub_category = models.CharField(choices=SUB_CATEGORIES, max_length=200, blank=True)
    code = models.CharField(max_length=200, blank=True)

    # Common fields across product categories
    width = models.IntegerField(null=True, blank=True, help_text="Unit of measure is mm")
    length = models.IntegerField(null=True, blank=True, help_text="Unit of measure is mm")
    heigth = models.IntegerField(null=True, blank=True, help_text="Unit of measure is mm, this is for geocells and drainage products")
    density = models.IntegerField(null=True, blank=True, help_text="Unit of measure is gsm, this is for geotextiles and GCL(Need to decide if this is for overall density or bentonite density)")

    title = models.CharField(max_length=200, blank=False)
    material = models.CharField(max_length=200, blank=True)
    short_description = models.TextField(blank=True)
    short_description.help_text = "This is a short concise and useful description of the product"
    long_description = models.TextField(blank=True)
    long_description.help_text = "This is for SEO purposes"
    applications = models.ManyToManyField(Application, related_name="products", blank=True)
    notes = models.TextField(blank=True)
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

    def get_product_detail_model(self):
        # Check which OneToOne relationship is set and return its associated model
        if self.product_detail_geocell:
            return self.product_detail_geocell
        elif self.product_detail_geotextile:
            return self.product_detail_geotextile
        elif self.product_detail_gcl:
            return self.product_detail_gcl
        elif self.product_detail_geogrid:
            return self.product_detail_geogrid
        elif self.product_detail_drainage:
            return self.product_detail_drainage
        return None

    def get_product_detail_name(self):
        detail_model = self.get_product_detail_model()
        if detail_model:
            return detail_model._meta.verbose_name
        return ""
    
    def get_default_image(self):
        default_media = self.media.filter(is_default=True, resource_type='product_image').first()
        return default_media.media if default_media else None

class Price(models.Model):
    date = models.DateField(default=date.today)
    qty = models.IntegerField()
    unit_of_measure = models.CharField(choices=UNITS_OF_MEASURE, max_length=200, default='sqm')
    comment = models.CharField(max_length=200, blank=True, null=True)
    FOB_port = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(choices=CURRENCIES, max_length=200, default='usd')
    expiry = models.DateField(blank=True, null=True, default=get_expiry_date())
    price = models.DecimalField(max_digits=7, decimal_places=2)
    base_product = models.ForeignKey(BaseProduct, on_delete=CASCADE, related_name='price')

class ProductMediaRelation(models.Model):
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='media')
    resource_type = models.CharField(choices=RESOURCE_TYPES, max_length=255)
    media_type = models.CharField(max_length=10, choices=(('image', 'Image'), ('document', 'Document')), default='image')
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Unset other main images for this product
            ProductMediaRelation.objects.filter(product=self.product).update(is_default=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.resource_type} for {self.product.code}"


class ProductEnquiry(models.Model):
    CHOICES = (
        ('YES', 'Yes'),
        ('NO', 'No'),
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    existing_customer = models.CharField(choices=CHOICES, max_length=15)
    product_interested_in = models.CharField(max_length=200)
    estimated_quantity = models.CharField(max_length=50)
    specifications = models.TextField(blank=True)
    project_based = models.TextField(blank=True)
    needed_by = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Enquiries"



