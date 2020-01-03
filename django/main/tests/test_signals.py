from django.test import TestCase
from main import models
from django.core.files.images import ImageFile
from decimal import Decimal
import logging


class TestThumbnailSignals(TestCase):
    def test_thumbnails_are_created_on_save(self):
        product = models.Product(
            name="The cathedral and the bazaar",
            price=Decimal("20.00")
        )
        product.save()

        with open("main/fixtures/the-cathedral-the-bazaar.jpg", "rb") as f:
            image = models.ProductImage(
                product=product,
                image=ImageFile(f, name="tctb.jpg"),
            )
            logger = logging.getLogger("main")
            with self.assertLogs(logger, level="INFO") as cm:
                image.save()

            self.assertGreaterEqual(len(cm.output), 1)
            image.refresh_from_db()

            with open("main/fixtures/the-cathedral-the-bazaar.thumb.jpg", "rb") as tn:
                expected_content = tn.read()
                thumbnail = image.thumbnail.read()
                assert thumbnail == expected_content

            image.thumbnail.delete(save=False)
            image.image.delete(save=False)

