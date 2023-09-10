from rest_framework import serializers

from products import models as product_models
from products import services as product_services


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.Application
        fields = ['name', 'description']


class DrainagePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.DrainagePrice
        fields = '__all__'


class GCLPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GCLPrice
        fields = '__all__'


class GeoCellPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GeoCellPrice
        fields = '__all__'


class GeoGridPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GeoGridPrice
        fields = '__all__'


class GeoTextilePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GeoTextilePrice
        fields = '__all__'


class DrainageSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = DrainagePriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()

    class Meta:
        model = product_models.Drainage
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'sub_categories', 'type', 'height', 'roll_width', 'double_cuspated',
                  'applications', 'prices', 'active_price']

    def get_active_price(self, obj):
        service = product_services.DrainageService(obj)
        return service.get_active_price()


class GCLSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = GCLPriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()

    class Meta:
        model = product_models.GCL
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'sub_categories', 'density', 'roll_width', 'roll_length', 'bentonite_specs',
                  'applications', 'prices', 'active_price']

    def get_active_price(self, obj):
        service = product_services.DrainageService(obj)
        return service.get_active_price()


class GeoCellSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = GeoCellPriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()

    class Meta:
        model = product_models.GeoCell
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'sub_categories', 'height', 'weld_spacing', 'is_textured', 'applications',
                  'prices', 'active_price']

    def get_active_price(self, obj):
        service = product_services.DrainageService(obj)
        return service.get_active_price()


class GeoGridSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = GeoGridPriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()

    class Meta:
        model = product_models.GeoGrid
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'sub_categories', 'shape', 'strength_md', 'strength_td', 'applications',
                  'prices', 'active_price']

    def get_active_price(self, obj):
        service = product_services.DrainageService(obj)
        return service.get_active_price()


class GeoTextileSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = GeoTextilePriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()

    class Meta:
        model = product_models.GeoTextile
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'sub_categories', 'density', 'roll_width', 'roll_length', 'type',
                  'applications', 'prices', 'active_price']

    def get_active_price(self, obj):
        service = product_services.DrainageService(obj)
        return service.get_active_price()
