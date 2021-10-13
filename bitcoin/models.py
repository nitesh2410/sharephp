from django.db import models

# Create your models here.
class Buy_sell_data(models.Model):
    datadate = models.DateTimeField()
    coin = models.CharField(max_length=200)
    price = models.FloatField()
    volume = models.FloatField()
    amount = models.FloatField()
    trade = models.CharField(max_length=200)

class coin_average(models.Model):
    coin = models.CharField(max_length=200)
    volume = models.FloatField()
    amount = models.FloatField()
    average = models.FloatField()
    TotalProfit = models.FloatField()
    alltime_high = models.FloatField()
    percent_down = models.CharField(max_length=20)
    currentprice = models.FloatField()
    profit_loss = models.FloatField()

class coin_gecho(models.Model):
    coin = models.CharField(max_length=200)
    coinsearch = models.CharField(max_length=200)


