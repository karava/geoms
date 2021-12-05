from django.contrib import admin
from .models import Geocell, BaseProduct, DatasheetFile, TestingFile, ImageFile, Price, Geotextile, GCL, DrainageProduct, Geogrid
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
class BaseProductInline(nested_admin.NestedStackedInline):
    model = BaseProduct
    extra = 1
    inlines = [DatasheetFileInLine, TestingFileInLine, ImageFileInLine, PriceInLine]

# Main
class GeocellAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]

class GeotextileAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]

class GCLAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]

class GeogridAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]
class DrainageAdmin(nested_admin.NestedModelAdmin):
    inlines = [BaseProductInline]

# Register your models here.
admin.site.register(Geocell, GeocellAdmin)
admin.site.register(Geotextile, GeotextileAdmin)
admin.site.register(GCL, GCLAdmin)
admin.site.register(Geogrid, GeogridAdmin)
admin.site.register(DrainageProduct, DrainageAdmin)