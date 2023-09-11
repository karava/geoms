from rest_framework import viewsets

from products import models as product_models
from products import serializers as product_serializers
from products import filters


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = product_models.Application.objects.all()
    serializer_class = product_serializers.ApplicationSerializer


class DrainageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = product_models.Drainage.objects.all()
    serializer_class = product_serializers.DrainageSerializer
    filterset_class = filters.DrainageFilter


class GCLViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = product_models.GCL.objects.all()
    serializer_class = product_serializers.GCLSerializer
    filterset_class = filters.GCLFilter


class GeoCellViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = product_models.GeoCell.objects.all()
    serializer_class = product_serializers.GeoCellSerializer
    filterset_class = filters.GeoCellFilter


class GeoGridViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = product_models.GeoGrid.objects.all()
    serializer_class = product_serializers.GeoGridSerializer
    filterset_class = filters.GeoGridFilter


class GeoTextileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = product_models.GeoTextile.objects.all()
    serializer_class = product_serializers.GeoTextileSerializer
    filterset_class = filters.GeoTextileFilter
