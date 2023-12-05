from django.contrib import admin
from .models import BaseProduct, ProductMediaRelation, Price, Application, ProductEnquiry
import nested_admin
from tinymce.widgets import TinyMCE
from django.db import models

class ProductRelationInline(nested_admin.NestedTabularInline):
    model = ProductMediaRelation
    extra = 1

class PriceInLine(nested_admin.NestedTabularInline):
    model = Price
    extra = 1

class BaseProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductRelationInline, PriceInLine]
    filter_horizontal = ('applications',)
    save_as = True

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'long_description':
    #         kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs=mce_attrs)
    #     return super().formfield_for_dbfield(db_field, **kwargs)

# Register your models here.
admin.site.register(BaseProduct, BaseProductAdmin)
admin.site.register(Application)
admin.site.register(ProductEnquiry)