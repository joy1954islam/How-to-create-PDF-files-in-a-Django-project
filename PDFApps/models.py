from django.db import models
from django.utils import timezone


class Customer(models.Model):
    Product_name = models.CharField(max_length=100)
    logo = models.ImageField(blank=True, upload_to='Logo', default='photo.jpg')
    description = models.TextField()
    quality = models.IntegerField()
    price = models.FloatField()
    Sale_Date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Product_name

    def total_price(self):
        return self.quality * self.price
