from django.db import models
from .generic_managers import ActiveManager


class ProductTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class ProductTag(models.Model):

    objects = ProductTagManager()

    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)


class Product(models.Model):

    objects = ActiveManager()

    tags = models.ManyToManyField(ProductTag, blank=True)
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=48)
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-images')
    thumbnail = models.ImageField(upload_to='product-thumbnails', null=True)
