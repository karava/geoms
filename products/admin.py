from django.contrib import admin
from .models import Geocell, BaseProduct, ProductModelImageRelation, Price, Geotextile, GCL, DrainageProduct, Geogrid, ProductResource, Application, ProductEnquiry
import nested_admin
from tinymce.widgets import TinyMCE
from django.db import models

# Inline Inlines
# class ImageFileInLine(nested_admin.NestedStackedInline):
#     model = ImageFile
#     extra = 1

class ProductImageRelationInline(nested_admin.NestedStackedInline):
    model = ProductModelImageRelation
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
    inlines = [ProductImageRelationInline, PriceInLine, ProductResourceInline]
    filter_horizontal = ('applications',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'long_description':
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return super().formfield_for_dbfield(db_field, **kwargs)

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
admin.site.register(ProductEnquiry)