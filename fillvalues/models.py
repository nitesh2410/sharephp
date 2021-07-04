from django.db import models

# Create your models here.

class Company(models.Model):
    company = models.CharField(max_length=200, unique=True)
    search_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    sectorsearch = models.CharField(max_length=100)
    priceshortsearch = models.CharField(default=0, max_length=100)
    exchange = models.CharField(default='N', max_length=100)

    def __str__(self):
        return self.company


class sharePrice(models.Model):
    pricedate = models.DateField()
    openprice = models.FloatField()
    closeprice = models.FloatField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)


class ShareCheckList(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    buyprice = models.FloatField()
    buydate = models.DateField()


class ShareWatchList(models.Model):
    watchprice = models.FloatField()
    watchdate = models.DateField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)