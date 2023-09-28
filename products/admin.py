from django.contrib import admin
from .models import Geocell, BaseProduct, ImageFile, Price, Geotextile, GCL, DrainageProduct, Geogrid, ProductResource, Application
import nested_admin

# Inline Inlines
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
    inlines = [ImageFileInLine, PriceInLine, ProductResourceInline]
    filter_horizontal = ('applications',)

# Main
class GeocellAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]
    save_as = True

class GeotextileAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]
    save_as = True

class GCLAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]
    save_as = True

class GeogridAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]
    save_as = True
    
class DrainageAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]
    save_as = True

# Register your models here.
admin.site.register(Geocell, GeocellAdmin)
admin.site.register(Geotextile, GeotextileAdmin)
admin.site.register(GCL, GCLAdmin)
admin.site.register(Geogrid, GeogridAdmin)
admin.site.register(DrainageProduct, DrainageAdmin)
admin.site.register(Application)