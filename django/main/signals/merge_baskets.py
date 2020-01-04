import logging
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from main.models import Basket

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def merge_baskets_if_found(sender, user, request, **kwargs):
    anonymous_basket = getattr(request, 'basket', None)
    if anonymous_basket:
        try:
            loggedin_basket = Basket.objects.get(
                user=user, status=Basket.OPEN
            )
            for line in anonymous_basket.basketline_set.all():
                line.basket = loggedin_basket
                line.save()
            anonymous_basket.delete()
            request.basket = loggedin_basket
            logger.info('Merged basked for user %s', user.email)

        except Basket.DoesNotExist:
            anonymous_basket.user = user
            anonymous_basket.save()
            logger.info("Assigned anonymous basket to user %s", user.email)
