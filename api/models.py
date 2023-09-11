from django.db import models

# Create your models here.


class Store(models.Model):
    date = models.IntegerField(blank=True, null=True)
    scrip = models.CharField(max_length=15, blank=True, null=True)
    openingPrice = models.FloatField(max_length=15, blank=True, null=True)
    highPrice = models.FloatField(max_length=15, blank=True, null=True)
    lowPrice = models.FloatField(max_length=15, blank=True, null=True)
    closingPrice = models.FloatField(max_length=15, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.scrip)
