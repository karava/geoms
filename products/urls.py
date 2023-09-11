from django.urls import path, include
from rest_framework import routers

from products import views as products_views

router = routers.DefaultRouter()
router.register(r'application', products_views.ApplicationViewSet)
router.register(r'drainage', products_views.DrainageViewSet)
router.register(r'gcl', products_views.GCLViewSet)
router.register(r'geocell', products_views.GeoCellViewSet)
router.register(r'geogrid', products_views.GeoGridViewSet)
router.register(r'geotextile', products_views.GeoTextileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
