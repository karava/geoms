import django_filters
from products import models as product_models


class BaseProductFilter(django_filters.FilterSet):
    applications = django_filters.CharFilter(method='filter_applications')

    def filter_applications(self, queryset, name, value):
        applications = value.split(',')
        return queryset.filter(applications__name__in=applications)


class DrainageFilter(BaseProductFilter):
    class Meta:
        model = product_models.Drainage
        fields = ['sub_category']


class GCLFilter(BaseProductFilter):
    class Meta:
        model = product_models.GCL
        fields = ['sub_category']


class GeoCellFilter(BaseProductFilter):
    class Meta:
        model = product_models.GeoCell
        fields = []


class GeoGridFilter(BaseProductFilter):
    class Meta:
        model = product_models.GeoGrid
        fields = ['sub_category']


class GeoTextileFilter(BaseProductFilter):
    class Meta:
        model = product_models.GeoTextile
        fields = ['sub_category']
