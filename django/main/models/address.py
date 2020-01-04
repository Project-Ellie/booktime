from django.db import models
from main.models import User


class Address(models.Model):
    SUPPORTED_COUNTRIES = (
        ('uk', 'United Kingdom'),
        ('us', 'United States of America'),
        ('ch', 'Switzerland'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    address1 = models.CharField('Address line 1', max_length=60)
    address2 = models.CharField('Address line 2', max_length=60, blank=True)
    zip_code = models.CharField('Zip/Postal Code', max_length=12)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=3, choices=SUPPORTED_COUNTRIES)

    def __str__(self):
        return ", ".join([
            self.name,
            self.address1,
            self.zip_code,
            self.city,
            self.country,
        ]
        )
