from django.contrib import admin
from .models import Product, ProductMediaRelation, Application, ProductEnquiry
import nested_admin
from tinymce.widgets import TinyMCE
from django.db import models

class ProductRelationInline(nested_admin.NestedTabularInline):
    model = ProductMediaRelation
    extra = 1

class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductRelationInline]
    filter_horizontal = ('applications',)
    readonly_fields = ('created_at', 'updated_at')
    
    ## Allows save as to be enabled so that we can duplicate products
    save_as = True

    list_display = ('code', 'title', 'category', 'sub_category', 'updated_at')  # Adjust as needed
    list_filter = ('category',)  # Add category to the list of filters
    list_display_links = ('code', 'title')

    search_fields = (
        'code',                         # exact match or prefix match
        'title__icontains',             # title contains …
    )
    search_help_text = (
        "Search by product code or title."
    )
    
    exclude = ('applications',)

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if db_field.name == 'long_description':
    #         kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs=mce_attrs)
    #     return super().formfield_for_dbfield(db_field, **kwargs)

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Application)
admin.site.register(ProductEnquiry)