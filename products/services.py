from django.utils import timezone

from products import models as product_models


class BaseService:
    """Product related"""
    def __init__(self, obj):
        """set the instance
        :param obj: the product instance
        :type obj: Product
        """
        self.obj = obj

    def get_active_price(self):
        """Product might have multiple price for same date range, only the latest one is active"""
        now = timezone.now()
        active_price = self.obj.prices.filter(date__lt=now, expiry__gt=now).order_by('-id').first()
        if active_price:
            return active_price.price
        else:
            return None


class DrainageService(BaseService):
    model = product_models.Drainage


class GCLService(BaseService):
    model = product_models.GCL


class GeoCellService(BaseService):
    model = product_models.GeoCell


class GeoGridService(BaseService):
    model = product_models.GeoGrid


class GeoTextileService(BaseService):
    model = product_models.GeoTextile
