from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from products import models as product_models
from products.services import DrainageService


class DrainageServiceTestCase(TestCase):
    def setUp(self) -> None:
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        tomorrow = now + timedelta(days=1)
        product1 = product_models.Drainage.objects.create(title='t', height=10, roll_width=20)
        product_models.DrainagePrice.objects.create(start_at=yesterday, qty=1, expiry_at=tomorrow, price=100,
                                                    product=product1)
        product_models.DrainagePrice.objects.create(start_at=yesterday, qty=1, expiry_at=tomorrow, price=200,
                                                    product=product1)
        product_models.DrainageImage.objects.create(
            is_for_website=True,
            is_default=False,
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content='',
                content_type='image/jpeg'
            ),
            product=product1
        )
        self.product1 = product1

    def test_get_active_price(self):
        active_price = DrainageService(self.product1).get_active_price()
        self.assertEqual(active_price, 200)

    def test_get_default_image(self):
        default_image_url = DrainageService(self.product1).get_default_image()
        self.assertEqual(default_image_url, '')
