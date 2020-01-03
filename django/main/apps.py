from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from . import signals
        logger.info("Loaded signals, a.o. for %s", signals.ProductImage)
