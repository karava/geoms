import os
from django.db import models
from django.db.models import base
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, BooleanField, DecimalField, IntegerField
from datetime import date, timedelta
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from knowledge_base.models import Media
from storage_backends import PublicMediaStorage
from django.utils.timezone import now

# Functions
def get_expiry_date():
    return date.today() + timedelta(days=30)

# Choices (right side side is human readable, left side is the value stored in the database)
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
    ('geomembrane', 'GCL - Geomembrane'),
    ('biaxial', 'Geogrid - Biaxial'),
    ('triaxial', 'Geogrid - Triaxial'),
    ('composite', 'Geogrid - Composite Biaxial'),
    ('woven', 'Geotextile - Woven'),
    ('nonwoven', 'Geotextile - Non-woven'),
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

class Product(models.Model):
    category = models.CharField(choices=CATEGORIES, max_length=200, blank=False)
    sub_category = models.CharField(choices=SUB_CATEGORIES, max_length=200, blank=True)
    code = models.CharField(max_length=200, blank=True)

    title = models.CharField(max_length=200, blank=False)
    short_description = models.TextField(blank=True)
    short_description.help_text = "This is a short concise and useful description of the product"
    long_description = models.TextField(blank=True)
    long_description.help_text = "This is for SEO purposes, roughly 500 words"
    applications = models.ManyToManyField(Application, related_name="products", blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_default_image(self):
        default_media = self.media.filter(is_default=True, resource_type='product_image').first()
        return default_media.media if default_media else None
    
    def __str__(self):
        return self.code

    def get_absolute_url(self):
        # Map singular database values to plural URL slugs
        category_to_plural = {
            'geocell': 'geocells',
            'gcl': 'gcls',
            'geotextile': 'geotextiles',
            'geogrid': 'geogrids',
            'drainage': 'drainage',  # stays singular
        }
        plural_category = category_to_plural.get(self.category, self.category)
        return reverse("products:product_detail", kwargs={"category_slug": plural_category, "product_code": self.code})

class ProductMediaRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    resource_type = models.CharField(choices=RESOURCE_TYPES, max_length=255)
    media_type = models.CharField(max_length=10, choices=(('image', 'Image'), ('document', 'Document')), default='image')
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    alt_text = models.CharField(max_length=255, blank=True, null=True, help_text="Alternative text for SEO and accessibility.")

    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Unset other main images for this product
            ProductMediaRelation.objects.filter(product=self.product).update(is_default=False)
        # Only set alt_text if it is blank (i.e. user hasn't manually provided one)
        # and there's a valid media file name
        if not self.alt_text and self.media and self.media.file and self.media.file.name:
            # Extract file name, remove extension, replace underscores
            base_name = os.path.basename(self.media.file.name)      # e.g. "my_image_file.jpg"
            base, ext = os.path.splitext(base_name)                 # base="my_image_file", ext=".jpg"
            base = base.replace("_", " ")                           # "my image file"
            self.alt_text = base
        super().save(*args, **kwargs)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.resource_type} for {self.product.code}"


class ProductEnquiry(models.Model):
    CHOICES = (
        ('YES', 'Yes'),
        ('NO', 'No'),
    )
    full_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
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



