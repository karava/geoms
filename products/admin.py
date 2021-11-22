from django.contrib import admin
from .models import Geocell, BaseProduct

class BaseProductInline(admin.StackedInline):
    model = BaseProduct
    extra = 1

class GeocellAdmin(admin.ModelAdmin):
    inlines = [BaseProductInline]

# Register your models here.
admin.site.register(Geocell, GeocellAdmin)