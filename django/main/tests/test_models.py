from decimal import Decimal

from django.test import TestCase
from main import models


class TestProduct(TestCase):

    def test_active_manager_works(self):
        models.Product.objects.create(
            name="P1",
            price=Decimal("20.00")
        )
        models.Product.objects.create(
            name="P2",
            price=Decimal("10.00"),
            active=False
        )
        models.Product.objects.create(
            name="P3",
            price=Decimal("15.00")
        )
        self.assertEquals(len(models.Product.objects.active()), 2)
