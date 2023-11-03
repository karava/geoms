from django.contrib import admin
from .models import Geocell, BaseProduct, ProductMediaRelation, Price, Geotextile, GCL, DrainageProduct, Geogrid,Application, ProductEnquiry
import nested_admin
from tinymce.widgets import TinyMCE
from django.db import models

class ProductRelationInline(nested_admin.NestedTabularInline):
    model = ProductMediaRelation
    extra = 1

class PriceInLine(nested_admin.NestedTabularInline):
    model = Price
    extra = 1

class BaseProductInline(nested_admin.NestedStackedInline):
    model = BaseProduct
    extra = 1
    inlines = [ProductRelationInline, PriceInLine]
    filter_horizontal = ('applications',)

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'long_description':
    #         kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs=mce_attrs)
    #     return super().formfield_for_dbfield(db_field, **kwargs)

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