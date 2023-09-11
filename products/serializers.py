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


class DrainageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.DrainageImage
        fields = '__all__'


class GCLImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GCLImage
        fields = '__all__'


class GeoCellImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GeoCellImage
        fields = '__all__'


class GeoGridImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GeoGridImage
        fields = '__all__'


class GeoTextileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GeoTextileImage
        fields = '__all__'


class DrainageResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.DrainageResource
        fields = '__all__'


class GCLResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GCLResource
        fields = '__all__'


class GeoCellResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GeoCellResource
        fields = '__all__'


class GeoGridResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GeoGridResource
        fields = '__all__'


class GeoTextileResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.GeoTextileResource
        fields = '__all__'


class DrainageSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = DrainagePriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()
    images = DrainageImageSerializer(many=True, read_only=True)
    default_image = serializers.SerializerMethodField()
    resources = DrainageResourceSerializer(many=True, read_only=True)

    class Meta:
        model = product_models.Drainage
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'category', 'sub_category', 'height', 'roll_width', 'double_cuspated',
                  'applications', 'prices', 'active_price', 'images', 'default_image', 'resources']

    def get_active_price(self, obj):
        service = product_services.DrainageService(obj)
        return service.get_active_price()

    def get_default_image(self, obj):
        service = product_services.DrainageService(obj)
        return service.get_default_image()


class GCLSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = GCLPriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()
    images = DrainageImageSerializer(many=True, read_only=True)
    default_image = serializers.SerializerMethodField()
    resources = GCLResourceSerializer(many=True, read_only=True)

    class Meta:
        model = product_models.GCL
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'sub_category', 'density', 'roll_width', 'roll_length', 'bentonite_specs',
                  'applications', 'prices', 'active_price', 'images', 'default_image', 'resources']

    def get_active_price(self, obj):
        service = product_services.GCLService(obj)
        return service.get_active_price()

    def get_default_image(self, obj):
        service = product_services.GCLService(obj)
        return service.get_default_image()


class GeoCellSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = GeoCellPriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()
    images = DrainageImageSerializer(many=True, read_only=True)
    default_image = serializers.SerializerMethodField()
    resources = GeoCellResourceSerializer(many=True, read_only=True)

    class Meta:
        model = product_models.GeoCell
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'height', 'weld_spacing', 'is_textured', 'applications',
                  'prices', 'active_price', 'images', 'default_image', 'resources']

    def get_active_price(self, obj):
        service = product_services.GeoCellService(obj)
        return service.get_active_price()

    def get_default_image(self, obj):
        service = product_services.GeoCellService(obj)
        return service.get_default_image()


class GeoGridSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = GeoGridPriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()
    images = DrainageImageSerializer(many=True, read_only=True)
    default_image = serializers.SerializerMethodField()
    resources = GeoGridResourceSerializer(many=True, read_only=True)

    class Meta:
        model = product_models.GeoGrid
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'sub_category', 'shape', 'strength_md', 'strength_td', 'applications',
                  'prices', 'active_price', 'images', 'default_image', 'resources']

    def get_active_price(self, obj):
        service = product_services.GeoGridService(obj)
        return service.get_active_price()

    def get_default_image(self, obj):
        service = product_services.GeoGridService(obj)
        return service.get_default_image()


class GeoTextileSerializer(serializers.ModelSerializer):
    applications = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    prices = GeoTextilePriceSerializer(many=True, read_only=True)
    active_price = serializers.SerializerMethodField()
    images = DrainageImageSerializer(many=True, read_only=True)
    default_image = serializers.SerializerMethodField()
    resources = GeoTextileResourceSerializer(many=True, read_only=True)

    class Meta:
        model = product_models.GeoTextile
        fields = ['code', 'title', 'material', 'short_description', 'long_description', 'notes', 'suppliers',
                  'unit_of_measure', 'twentygp_cap', 'fortygp_cap', 'fortyhc_cap', 'moq', 'alternative_names',
                  'packing_description', 'density', 'roll_width', 'roll_length', 'category', 'sub_category',
                  'applications', 'prices', 'active_price', 'images', 'default_image', 'resources']

    def get_active_price(self, obj):
        service = product_services.GeoTextileService(obj)
        return service.get_active_price()

    def get_default_image(self, obj):
        service = product_services.GeoTextileService(obj)
        return service.get_default_image()
