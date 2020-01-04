import logging
from decimal import Decimal

from django.test import TestCase
from main import models, factories


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

    def test_create_order_works(self):
        p1 = factories.ProductFactory()
        p2 = factories.ProductFactory()
        user1 = factories.UserFactory()
        billing = factories.AddressFactory(user=user1)
        shipping = factories.AddressFactory(user=user1)

        basket = models.Basket.objects.create(user=user1)
        models.BasketLine.objects.create(
            basket=basket, product=p1
        )
        models.BasketLine.objects.create(
            basket=basket, product=p2
        )

        with self.assertLogs(logging.getLogger("main.models"), level="INFO") as cm:
            order = basket.create_order(billing, shipping)

        self.assertGreaterEqual(len(cm.output), 1)

        order.refresh_from_db()

        self.assertEquals(order.user, user1)
        self.assertEquals(
            order.billing_address1, billing.address1
        )
        self.assertEquals(
            order.shipping_address1, shipping.address1
        )

        self.assertEquals(order.lines.all().count(), 2)
        lines = order.lines.all()
        self.assertEquals(lines[0].product, p1)
        self.assertEquals(lines[1].product, p2)
