from django.contrib import admin
from .models import Product, ProductMediaRelation, Price, Application, ProductEnquiry
import nested_admin
from tinymce.widgets import TinyMCE
from django.db import models

class ProductRelationInline(nested_admin.NestedTabularInline):
    model = ProductMediaRelation
    extra = 1

class PriceInLine(nested_admin.NestedTabularInline):
    model = Price
    extra = 1

class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductRelationInline, PriceInLine]
    filter_horizontal = ('applications',)
    readonly_fields = ('created_at', 'updated_at')
    
    ## Allows save as to be enabled so that we can duplicate products
    save_as = True

    list_display = ('code', 'title', 'category', 'sub_category', 'updated_at')  # Adjust as needed
    list_filter = ('category',)  # Add category to the list of filters

    search_fields = (
        'code',                         # exact match or prefix match
        'title__icontains',             # title contains …
    )
    search_help_text = (
        "Search by product code or title."
    )

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'long_description':
    #         kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs=mce_attrs)
    #     return super().formfield_for_dbfield(db_field, **kwargs)
    def display_latest_price(self, obj):
        latest_price = obj.get_latest_price()
        if latest_price:
            return latest_price.price
        return 'No price set'

    display_latest_price.short_description = 'Latest Price'

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Application)
admin.site.register(ProductEnquiry)