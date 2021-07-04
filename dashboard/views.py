from django.shortcuts import render
from fillvalues.models import ShareCheckList, sharePrice
from django.db import connection
from django.db.models import Max

# Create your views here.

def index(request):
    share = ShareCheckList.objects.values('company_id','company_id__company','company_id__search_name', 'buyprice', 'buydate')
    mysharelist = []
    for slist in share:
        sprice = sharePrice.objects.values('pricedate','openprice','closeprice').filter(company_id=slist['company_id']).order_by('-pricedate')[0:9]
        if not sprice:
            mysharelist.append({'ShareName': slist['company_id__company'],
                                'SearchName': slist['company_id__search_name'],
                                'BuyDate': slist['buydate'],
                                'BuyPrice': slist['buyprice'],
                                'PriceDAte': '',
                                'OpenPrice': '',
                                'ClosePrice': '',
                                'sharepercen': 0



                                })
        else:
            sharepercen = (sprice[0]['closeprice'] - slist['buyprice'])*100/slist['buyprice']

            args = sharePrice.objects.filter(company_id=slist['company_id'])  # or whatever arbitrary queryset
            maxvalue = args.aggregate(Max('closeprice'))

            MAxsharepercen = round(( sprice[0]['closeprice'] - maxvalue['closeprice__max']) * 100 / maxvalue['closeprice__max'])

            last5daychng = []
            i = len(sprice) - 1;
            while i > 0:
                last5daychn = sprice[i-1]
                last5daychn['pricediff'] = round(sprice[i-1]['closeprice']-sprice[i]['closeprice'],2)
                last5daychn['ptage'] = round(( sprice[i-1]['closeprice']-sprice[i]['closeprice']) * 100 / sprice[i]['closeprice'],2)
                last5daychng.append(last5daychn)
                i = i-1


            print(last5daychng)

            mysharelist.append({'ShareName': slist['company_id__company'],
                                'SearchName': slist['company_id__search_name'],
                                'BuyDate': slist['buydate'],
                                'BuyPrice': slist['buyprice'],
                                'PriceDAte': sprice[0]['pricedate'],
                                'OpenPrice': sprice[0]['openprice'],
                                'ClosePrice': sprice[0]['closeprice'],
                                'MaxPrice': maxvalue['closeprice__max'],
                                'last5daychng': last5daychng,
                                'sharepercen': str(round(sharepercen,2))+ ' ('+ str(MAxsharepercen)+')'
                                })

    context = {
        'sharedetails': mysharelist,
    }
    return render(request, 'dashboard.html', context)
