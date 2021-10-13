'''
1 - donot to hyper  -
2 - just buy coin and hold only or sell time to time
3 - if any news comes then purchase and get 30% hike only
4 - when you exit - here not any proper buy and sell point when you sell or buy that is the perfect time for you
5 - 10000 - fund ready
6 - set points where do you exit/book profit time to time - 60 65 70 75 80 85 90 95
7 - donot stuck in single coin - if it gives profit exit now

Summary of all the 10 Tips mentioned:
1. 4:13 Always follow the trend, wait for trend reversal to follow the opposite trend.

2. 6:52 Note down your top 10 fav coins because before TA, FA is the important factor. Choose only those coins which has good potential for mass adoption or real use cases. You can never lose money on those coins in the long run if you HODL.

3. 10:06 Wait for big dips. Don't reenter trades often after booking profits. Its important to have a cooldown and enjoy some time with your profits. Dont be addicted.

4. 12:42 Always enter in parts and always sell in parts. Because you can never to what extend a coin rises or dips. This is called "Ladder Buy" or "Ladder Sell" and is one of the most efficient way to book profits and manage risks.

5.  13:54 Don't be addicted to trading. Many traders are students here or are taking trading as part time. Trading is often compared to gambling because of addiction. You lost track of what's going on in your life and most importantly you become more and more greedy. You are never happy with the profits and at the long run you will be depressed or you won't be a happy man. Never be addicted.

6. 15:49 Set small Targets! Don't always aim for the highest profit, aim for 5% or even 3% profits per trade. Rama's Bridge to Lanka was made with small stones, take this wisdom from Ramayana and apply it to trading. If you aim for high profits in one go, you will lose a lot of money or earn way less in the long run than aiming for small targets.

7.  16:43 Always trade in BTC pair. Because in crypto trading our main goal is to increase the amount of BTC we hold not the amount of USDT. BTC will always be in the up trend, USDT is always constant.

8.  17:49 Book profits always. Just like tip 6, after you get your small targets (Tip 6). Dont keep watching until the coin rises more. Book your profits and rest for a while until you open your next trade which is again Tip 3.

9.  18:26 Don't fall in love with the coin. Love the profits. Its common that many people gets attached to a coin that they absolutely love because of its fundamentals. But if you want to be a good trader you need to change your girlfriends (coins) every now and then. Because as a trader we need to look for opportunities which comes in various ways through various coins, NOT THROUGH ONLY ONE COIN.

10. 19:55 Patience and Satisfaction is important in trading. This is basically the culmination of Tip 3, Tip 4, Tip 5, Tip 6,  and Tip 8. To summarize it. After you book some good profits, take a 24 hour gap or just binge watch a series being happy about the fact that you earned enough today. Don't be greedy. Have patience and and be happy with how well you are doing already.
'''

from django.shortcuts import render
from .models import Buy_sell_data, coin_average, coin_gecho
from .resources import CoinResources
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from django.db import connection
import datetime
from bs4 import BeautifulSoup
import requests


# Create your views here.
def simple_upload(request):
    if request.method == 'POST':
        coinresources = CoinResources()
        dataset = Dataset()

        print(request)

        new_data = request.FILES['myfile']

        if not new_data.name.endswith('xlsx'):
            messages.info(request, 'plz use xlsx format')
            return render(request, 'upload.html')
        imported_data = dataset.load(new_data.read(),format='xlsx')
        for data in imported_data:
            print(data)

            data2  =  data[2].replace('INR', '')
            data3 = data[3]
            data5 = data[5]
            if 'USDT' in data[2]:

                data2 = data[2].replace('USDT', '')
                data3 = data[3] * 75.5
                data5 = data[5] * 75.5
                print(data2)

            value = Buy_sell_data(
                data[0], data[1], data2, data3, data[4], data5, data[6])
            value.save()
    return render(request, 'upload.html')


def getAvg(request):
    trades = Buy_sell_data.objects.values('datadate', 'coin', 'price', 'volume', 'amount', 'trade').filter(datadate__gte=datetime.date(2021, 6, 22)).exclude(coin='BTC')
    #print(trades)
    coinArr = {}

    cursor = connection.cursor()
    #cursor.execute("TRUNCATE TABLE `bitcoin_coin_average`")

    for trade in trades:
        if trade['coin'] not in coinArr.keys():
            coinArr.update({trade['coin']: {'volume': 0, 'amount': 0}})
        print(trade['volume'])
        print(trade['trade'])
        print(trade['coin'])



        if trade['trade'] == 'Sell':
            coinArr[trade['coin']]['volume'] = float("{:.2f}".format(coinArr[trade['coin']]['volume'])) - float("{:.2f}".format(trade['volume']))
            coinArr[trade['coin']]['amount'] = float("{:.2f}".format(coinArr[trade['coin']]['amount'])) - float("{:.2f}".format(trade['amount']))
        else:
            coinArr[trade['coin']]['volume'] = float("{:.2f}".format(coinArr[trade['coin']]['volume'])) + float("{:.2f}".format(trade['volume']))
            coinArr[trade['coin']]['amount'] = float("{:.2f}".format(coinArr[trade['coin']]['amount'])) + float("{:.2f}".format(trade['amount']))



        #print(coinArr[trade['coin']]['volume'])
        if float("{:.2f}".format(coinArr[trade['coin']]['volume'])) == 0.00:
            print(type(0.0))
            print(coinArr[trade['coin']]['volume'])
            coinArr[trade['coin']]['amount'] = 0.0
            print(coinArr[trade['coin']]['amount'])
            del(coinArr[trade['coin']])

    print(coinArr)

    for key, ca in coinArr.items():
        print(key)

        gecko = get_geco(key)
        print(gecko)
        percent_down = gecko[3]
        alltimehigh = float(gecko[2])
        currentprice = float(gecko[6])

       # currentprice = float(current_pr(key))

        #if key.endswith("INR"):
        alltimehigh = float(gecko[2]) * 75
        currentprice = float(gecko[6]) * 75


        newavg = (ca['amount'])/70;
        totalp = 0
        if ca['amount']< 0:
            newavg = 0
            totalp = ca['amount']
        avg = newavg/ca['volume'];

        profitloss = currentprice * ca['volume'] - ca['volume'] * avg


        value = coin_average(coin=key, volume=float("{:.2f}".format(ca['volume'])), amount=float("{:.2f}".format(newavg)), average=float("{:.2f}".format(avg)),TotalProfit=float("{:.2f}".format(totalp)),alltime_high = float("{:.2f}".format(alltimehigh)),percent_down = percent_down ,currentprice = float("{:.2f}".format(currentprice)) ,profit_loss = float("{:.2f}".format(profitloss)))
        value.save()

    return HttpResponse(1)


def current_pr(coin):
    pass

def get_geco(coins):

    #https://api.coinstats.app/public/v1/coins?skip=0&limit=25&currency=EUR
    #https: // api.coinstats.app / public / v1 / coins / bitcoin?currency = USDT
    #https: // documenter.getpostman.com / view / 5734027 / RzZ6Hzr3  # 948fea46-e93a-47f8-93d8-915583f7406d
    print(coins)
    #coins = coins.replace("USDT", "")
    #coins = coins.replace("INR", "")

    if coins == '':
        coins = 'USDT'

    coinObj = coin_gecho.objects.filter(coin=coins)
    if not coinObj:
        return [0,0,0,0,0,0,0,0]
    return [0, 0, 0, 0, 0, 0, 0, 0]
    print(coinObj[0].coinsearch)

    url = 'https://www.coingecko.com/en/' + coinObj[0].coinsearch
    print(url)

    x = requests.get(url)

    alltimehightext = 0
    currentprice = 1

    soup = BeautifulSoup(x.text, 'html.parser')

    for table in soup.find_all("table", class_="table b-b"):
        print(table)
        for tr in table.findAll("tr"):
            print(tr.th.text)
            print(tr.td.text)
            he = tr.th.text.strip()
            print(he)
            if he == 'All-Time High':
                alltimehightext  = tr.td.text

            if 'Price' in tr.th.text:
                currentprice = tr.td.text.strip()
    alltimeArr = alltimehightext.splitlines()

    alltimeArr.append(currentprice)

    print(alltimeArr)
    gecko = [x.replace('$', '').replace(',', '') for x in alltimeArr]
    return(gecko)






