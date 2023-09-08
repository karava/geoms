from django.contrib import admin
from .models import Geocell, BaseProduct, DatasheetFile, TestingFile, ImageFile, Price, Geotextile, GCL, DrainageProduct, Geogrid, GeocellSubcategory, GCLSubcategory, GeotextileSubcategory, GeogridSubcategory, DrainageProductSubcategory, ProductResource, Application
import nested_admin

# Inline Inlines
class DatasheetFileInLine(nested_admin.NestedStackedInline):
    model = DatasheetFile
    extra = 1
class TestingFileInLine(nested_admin.NestedStackedInline):
    model = TestingFile
    extra = 1
class ImageFileInLine(nested_admin.NestedStackedInline):
    model = ImageFile
    extra = 1

class PriceInLine(nested_admin.NestedTabularInline):
    model = Price
    extra = 1

# Inlines
class ProductResourceInline(nested_admin.NestedStackedInline):
    model = ProductResource
    extra = 1
class BaseProductInline(nested_admin.NestedStackedInline):
    model = BaseProduct
    extra = 1
    inlines = [DatasheetFileInLine, TestingFileInLine, ImageFileInLine, PriceInLine, ProductResourceInline]
    filter_horizontal = ('applications',)

# Subcategory Inlines
class GeocellSubcategoryInline(nested_admin.NestedStackedInline):
    model = GeocellSubcategory
    extra = 1

class GCLSubcategoryInline(nested_admin.NestedStackedInline):
    model = GCLSubcategory
    extra = 1

class GeotextileSubcategoryInline(nested_admin.NestedStackedInline):
    model = GeotextileSubcategory
    extra = 1

class GeogridSubcategoryInline(nested_admin.NestedStackedInline):
    model = GeogridSubcategory
    extra = 1

class DrainageProductSubcategoryInline(nested_admin.NestedStackedInline):
    model = DrainageProductSubcategory
    extra = 1

# Main
class GeocellAdmin(nested_admin.NestedModelAdmin):
    inlines = [GeocellSubcategoryInline, BaseProductInline]
    save_as = True

class GeotextileAdmin(nested_admin.NestedModelAdmin):
    inlines = [GeotextileSubcategoryInline, BaseProductInline]
    save_as = True

class GCLAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]
    save_as = True

class GeogridAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]
    save_as = True
    
class DrainageAdmin(nested_admin.NestedModelAdmin):
    inlines = [DrainageProductSubcategoryInline, BaseProductInline]
    save_as = True
    filter_horizontal = ('DrainageProductSubcategory',)

# Register your models here.
admin.site.register(Geocell, GeocellAdmin)
admin.site.register(Geotextile, GeotextileAdmin)
admin.site.register(GCL, GCLAdmin)
admin.site.register(Geogrid, GeogridAdmin)
admin.site.register(DrainageProduct, DrainageAdmin)
admin.site.register(Application)
admin.site.register(DrainageProductSubcategory)