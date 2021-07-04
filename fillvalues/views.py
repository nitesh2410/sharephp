from django.shortcuts import render, get_object_or_404
import requests
from bs4 import BeautifulSoup
from .models import Company,sharePrice, ShareCheckList
import datetime
import re
from django.db import connection
from django.http import HttpResponse

def getshareprice(request):
    scllist = ShareCheckList.objects.values('company_id__company', 'company_id__priceshortsearch')
    for scl in scllist:
        url = 'http://127.0.0.1:8000/fillvalues/dayprice/' + scl['company_id__priceshortsearch']
        x = requests.get(url)
        print(url)
    return render(request, 'datavalue.html')

def dayprice(request, slug):
    print(slug)
    #return HttpResponse(1)
    compObj = Company.objects.values('id', 'company','exchange').filter(priceshortsearch =slug)
    #print(connection.queries)
    print(compObj)
    companyid = compObj[0]['id']
    compname = compObj[0]['company']
    exchange = compObj[0]['exchange']

    sharePriceObj = sharePrice.objects.values('pricedate').filter(company_id_id=companyid).order_by('-pricedate')[0:1]

    todayDate = datetime.datetime.today()
    if not sharePriceObj.exists():
        NextDay_Date = datetime.datetime.today() - datetime.timedelta(days=365)
        print(NextDay_Date)
    else:

        d1 = datetime.datetime(todayDate.year, todayDate.month, todayDate.day)
        d2 = datetime.datetime(sharePriceObj[0]['pricedate'].year, sharePriceObj[0]['pricedate'].month,sharePriceObj[0]['pricedate'].day)

        delta = d1 - d2
        if delta.days == 1 and todayDate.weekday() == 5:
            return render(request, 'datavalue.html')
        elif delta.days == 2 and todayDate.weekday() == 6:
            return render(request, 'datavalue.html')
        elif d1 > d2:
            NextDay_Date = sharePriceObj[0]['pricedate'] + datetime.timedelta(days=1)

    compname1 = compname.replace(" ", "%20")
    #url = 'http://127.0.0.1:8000/fillvalues/dataval'

    file = 'hist_stock_result.php'
    if exchange == 'B':
        file = 'histstock.php'

    url = 'https://www.moneycontrol.com/stocks/'+file+'?ex='+exchange+'&sc_id=' + slug + '&mycomp=' + compname1
    print(url);
    myobj = {'frm_dy': NextDay_Date.day, 'frm_mth':  NextDay_Date.month, 'frm_yr':  NextDay_Date.year, 'to_dy': todayDate.day, 'to_mth': todayDate.month, 'to_yr': todayDate.year, 'x': '17', 'y': '6', 'hdn': 'daily'}
    print(myobj)

    #x = requests.get(url)
    x = requests.post(url, data=myobj)
    print(x)

    soup = BeautifulSoup(x.text, 'html.parser')
    table = soup.find("table", {'class': 'tblchart'})

    for tr in table.findAll("tr"):
        print(tr)
        thlist = list(tr.find_all("th"))
        if len(thlist):
            continue

        tdlist = list(tr.find_all("td"))
        print(tdlist)
        if len(tdlist):
            pricedate = datetime.datetime.strptime(tdlist[0].text, '%d-%m-%Y').strftime('%Y-%m-%d')
            s = sharePrice(company_id=Company.objects.get(id=companyid), pricedate=pricedate, openprice=tdlist[1].text, closeprice=tdlist[4].text)
            s.save()

        else:
            return HttpResponse(1)
    return HttpResponse(1)

def home(request):
    return render(request, 'home.html')

    compObj = Company.objects.values('id', 'company')
    for complist in compObj:
        companyid = complist['id']
        compname = complist['company']
        print(compname)

        compname1 = compname.replace(" ", "%20")
        url = 'https://www.moneycontrol.com/stocks/autosuggest.php?str=' + compname1
        print(url);
        x = requests.get(url)
        if x.text == '<ul class="suglist"></ul>':
            continue
        soup = BeautifulSoup(x.text, 'html.parser')
        table = soup.find("a")

        print(table['onclick'])

        t1 = table['onclick'].split("','")
        t2 = t1[1].split("'")
        print(t2[0])
        t = Company.objects.get(id=companyid)
        t.priceshortsearch = t2[0]  # change field
        t.save()

    return render(request, 'home.html')


    return render(request, 'home.html')
    sectorDict = {'Abrasives': 'abrasives', 'Aluminium': 'aluminium', 'Aquaculture': 'aquaculture',
            'Auto - 2 &amp; 3 Wheelers': 'auto-2-3-wheelers', 'Auto - Cars &amp; Jeeps': 'auto-cars-jeeps',
            'Auto - LCVs &amp; HCVs': 'auto-lcvs-hcvs', 'Auto - Tractors': 'auto-tractors',
            'Auto Ancillaries': 'auto-ancillaries', 'Banks - Private Sector': 'banks-private-sector',
            'Banks - Public Sector': 'banks-public-sector', 'Bearings': 'bearings',
            'Breweries &amp; Distilleries': 'breweries-distilleries',
            'Cables - Power &amp; Others': 'cables-power-others', 'Cables - Telephone': 'cables-telephone',
            'Castings &amp; Forgings': 'castings-forgings', 'Cement - Major': 'cement-major',
            'Cement - Mini': 'cement-mini',
            'Cement - Products &amp; Building Materials': 'cement-products-building-materials',
            'Ceramics &amp; Granite': 'ceramics-granite', 'Chemicals': 'chemicals', 'Cigarettes': 'cigarettes',
            'Compressors': 'compressors', 'Computers - Hardware': 'computers-hardware',
            'Computers - Software': 'computers-software',
            'Computers - Software - Training': 'computers-software-training',
            'Computers - Software Medium &amp; Small': 'computers-software-medium-small',
            'Construction &amp; Contracting - Civil': 'construction-contracting-civil',
            'Construction &amp; Contracting - Housing': 'construction-contracting-housing',
            'Construction &amp; Contracting - Real Estate': 'construction-contracting-real-estate',
            'Consumer Goods - Electronic': 'consumer-goods-electronic',
            'Consumer Goods - White Goods': 'consumer-goods-white-goods', 'Couriers': 'couriers',
            'Detergents': 'detergents',
            'Diamond Cutting &amp; Jewellery &amp; Precious Met...': 'diamond-cutting-jewellery-precious-metals',
            'Diversified': 'diversified', 'Domestic Appliances': 'domestic-appliances', 'Dry Cells': 'dry-cells',
            'Dyes &amp; Pigments': 'dyes-pigments',
            'Edible Oils &amp; Solvent Extraction': 'edible-oils-solvent-extraction',
            'Electric Equipment': 'electric-equipment', 'Electricals': 'electricals',
            'Electrodes &amp; Graphite': 'electrodes-graphite', 'Engineering': 'engineering',
            'Engineering - Heavy': 'engineering-heavy', 'Engines': 'engines', 'Fasteners': 'fasteners',
            'Fertilisers': 'fertilisers', 'Finance - General': 'finance-general',
            'Finance - Housing': 'finance-housing', 'Finance - Investments': 'finance-investments',
            'Finance - Leasing &amp; Hire Purchase': 'finance-leasing-hire-purchase',
            'Finance - Term Lending Institutions': 'finance-term-lending-institutions',
            'Food Processing': 'food-processing', 'Glass &amp; Glass Products': 'glass-glass-products',
            'Hospitals &amp; Medical Services': 'hospitals-medical-services', 'Hotels': 'hotels',
            'Infrastructure - General': 'infrastructure-general', 'Leather Products': 'leather-products',
            'Lubricants': 'lubricants', 'Machine Tools': 'machine-tools',
            'Media &amp; Entertainment': 'media-entertainment', 'Metals - Non Ferrous': 'metals-non-ferrous',
            'Mining &amp; Minerals': 'mining-minerals', 'Miscellaneous': 'miscellaneous',
            'Oil Drilling And Exploration': 'oil-drilling-and-exploration', 'Packaging': 'packaging',
            'Paints &amp; Varnishes': 'paints-varnishes', 'Paper': 'paper', 'Personal Care': 'personal-care',
            'Pesticides &amp; Agro Chemicals': 'pesticides-agro-chemicals', 'Petrochemicals': 'petrochemicals',
            'Pharmaceuticals': 'pharmaceuticals', 'Plantations - Tea &amp; Coffee': 'plantations-tea-coffee',
            'Plastics': 'plastics', 'Power - Generation &amp; Distribution': 'power-generation-distribution',
            'Power - Transmission &amp; Equipment': 'power-transmission-equipment',
            'Printing &amp; Stationery': 'printing-stationery', 'Pumps': 'pumps', 'Refineries': 'refineries',
            'Retail': 'retail', 'Rubber': 'rubber', 'Shipping': 'shipping',
            'Steel - CR &amp; HR Strips': 'steel-cr-hr-strips', 'Steel - GP &amp; GC Sheets': 'steel-gp-gc-sheets',
            'Steel - Large': 'steel-large', 'Steel - Medium &amp; Small': 'steel-medium-small',
            'Steel - Pig Iron': 'steel-pig-iron', 'Steel - Rolling': 'steel-rolling',
            'Steel - Sponge Iron': 'steel-sponge-iron', 'Steel - Tubes &amp; Pipes': 'steel-tubes-pipes',
            'Sugar': 'sugar', 'Telecommunications - Equipment': 'telecommunications-equipment',
            'Telecommunications - Service': 'telecommunications-service',
            'Textiles - Composite Mills': 'textiles-composite-mills',
            'Textiles - Cotton Blended': 'textiles-cotton-blended', 'Textiles - Denim': 'textiles-denim',
            'Textiles - General': 'textiles-general', 'Textiles - Hosiery &amp; Knitwear': 'textiles-hosiery-knitwear',
            'Textiles - Machinery': 'textiles-machinery', 'Textiles - Manmade': 'textiles-manmade',
             'Textiles - Processing': 'textiles-processing', 'Textiles - Readymade Apparels': 'textiles-readymade-apparels', 'Textiles - Spinning - Cotton Blended': 'textiles-spinning-cotton-blended', 'Textiles - Spinning - Synthetic Blended': 'textiles-spinning-synthetic-blended', 'Textiles - Synthetic &amp; Silk': 'textiles-synthetic-silk', 'Textiles - Terry Towels': 'textiles-terry-towels', 'Textiles - Weaving': 'textiles-weaving', 'Textiles - Woollen &amp; Worsted': 'textiles-woollen-worsted', 'Trading': 'trading', 'Transport &amp; Logistics': 'transport-logistics', 'Tyres': 'tyres', 'Vanaspati &amp; Oils': 'vanaspati-oils'}

    for sector, sectorsearch in sectorDict.items():
        print('https://www.moneycontrol.com/stocks/marketstats/sec_performance/nse/' + sectorsearch + '.html')
        r = requests.get('https://www.moneycontrol.com/stocks/marketstats/sec_performance/nse/' + sectorsearch + '.html')
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.find_all("span", class_="op_bl13"):
            href = item.a['href']
            li = list(href.split('/'))
            search_name = li[6]
            short_name = li[7]
            companyname = item.a.b.text

            if not Company.objects.filter(company=companyname).exists():
                c = Company(company=companyname, search_name=search_name,short_name=short_name,sector=sector,sectorsearch=sectorsearch)
                c.save()
    return render(request, 'home.html')

def dataval(request):
    return render(request, 'datavalue.html')
