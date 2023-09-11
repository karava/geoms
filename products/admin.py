from django.contrib import admin

from products import models as product_models
from products import services as product_services


# Price Inlines
class DrainagePriceInline(admin.TabularInline):
    model = product_models.DrainagePrice
    can_delete = False
    extra = 1


class GCLPriceInline(admin.TabularInline):
    model = product_models.GCLPrice
    can_delete = False
    extra = 1


class GeoCellPriceInline(admin.TabularInline):
    model = product_models.GeoCellPrice
    can_delete = False
    extra = 1


class GeoGridPriceInline(admin.TabularInline):
    model = product_models.GeoGridPrice
    can_delete = False
    extra = 1


class GeoTextilePriceInline(admin.TabularInline):
    model = product_models.GeoTextilePrice
    can_delete = False
    extra = 1


# Image Inlines
class DrainageImageInline(admin.TabularInline):
    model = product_models.DrainageImage
    extra = 1


class GCLImageInline(admin.TabularInline):
    model = product_models.GCLImage
    extra = 1


class GeoCellImageInline(admin.TabularInline):
    model = product_models.GeoCellImage
    extra = 1


class GeoGridImageInline(admin.TabularInline):
    model = product_models.GeoGridImage
    extra = 1


class GeoTextileImageInline(admin.TabularInline):
    model = product_models.GeoTextileImage
    extra = 1


# Resource Inlines
class DrainageResourceInline(admin.TabularInline):
    model = product_models.DrainageResource
    extra = 1


class GCLResourceInline(admin.TabularInline):
    model = product_models.GCLResource
    extra = 1


class GeoCellResourceInline(admin.TabularInline):
    model = product_models.GeoCellResource
    extra = 1


class GeoGridResourceInline(admin.TabularInline):
    model = product_models.GeoGridResource
    extra = 1


class GeoTextileResourceInline(admin.TabularInline):
    model = product_models.GeoTextileResource
    extra = 1


# Main
@admin.register(product_models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short')

    @admin.display(description='Desc')
    def description_short(self, obj):
        return obj.description[:64] if obj.description else ''


@admin.register(product_models.Drainage)
class DrainageAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'suppliers', 'category', 'sub_category', 'height', 'roll_width', 'active_price')
    search_fields = ['category', 'code', 'title', 'suppliers']
    inlines = [DrainagePriceInline, DrainageImageInline, DrainageResourceInline]
    save_as = True

    @admin.display(description='Active Price')
    def active_price(self, obj):
        service = product_services.DrainageService(obj)
        return service.get_active_price()


@admin.register(product_models.GCL)
class GCLAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'suppliers', 'density', 'roll_width', 'roll_length', 'bentonite_specs',
                    'sub_category', 'active_price')
    search_fields = ['bentonite_specs', 'code', 'title', 'suppliers']
    inlines = [GCLPriceInline, GCLImageInline, GCLResourceInline]
    save_as = True

    @admin.display(description='Active Price')
    def active_price(self, obj):
        service = product_services.GCLService(obj)
        return service.get_active_price()


@admin.register(product_models.GeoCell)
class GeocellAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'suppliers', 'height', 'weld_spacing', 'is_textured', 'active_price')
    search_fields = ['code', 'title', 'suppliers']
    inlines = [GeoCellPriceInline, GeoCellImageInline, GeoCellResourceInline]
    save_as = True

    @admin.display(description='Active Price')
    def active_price(self, obj):
        service = product_services.GeoCellService(obj)
        return service.get_active_price()


@admin.register(product_models.GeoGrid)
class GeogridAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'suppliers', 'shape', 'strength_md', 'strength_td', 'sub_category', 'active_price')
    search_fields = ['shape', 'code', 'title', 'suppliers']
    inlines = [GeoGridPriceInline, GeoGridImageInline, GeoGridResourceInline]
    save_as = True

    @admin.display(description='Active Price')
    def active_price(self, obj):
        service = product_services.GeoGridService(obj)
        return service.get_active_price()


@admin.register(product_models.GeoTextile)
class GeoTextileAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'suppliers', 'density', 'roll_width', 'roll_length', 'category', 'sub_category',
                    'active_price')
    search_fields = ['category', 'code', 'title', 'suppliers']
    inlines = [GeoTextilePriceInline, GeoTextileImageInline, GeoTextileResourceInline]
    save_as = True

    @admin.display(description='Active Price')
    def active_price(self, obj):
        service = product_services.GeoTextileService(obj)
        return service.get_active_price()
