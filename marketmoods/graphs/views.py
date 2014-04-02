from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Template, Context
from django.db.models import Q

from valence.models import Company, Price

import datetime,json,pdb
import pytz
import evaluate

class Industry(object):
    name = ""
    companies = []
    toggled = False
    data = []


today = datetime.datetime.today()
master_industries = []
charted_industries = {}
master_companies = []
charted_companies = {}

def get_current_data():
    master_data = []
    if len(charted_industries):
        data_list = []
        for entry in charted_industries:
            data_list.append(charted_industries[entry])
        return [data_list]
    else:
        return [[[[0, 0], [100, 0]], [[0, 100],[100,0]]]]


def industry_for_name(name):
    for ind in master_industries:
        if name == ind.name:
            return ind
    newInd = Industry()
    newInd.name = name
    return newInd

def format_name_for_display(ticker,name):
    ticker = '['+ticker+'] '
    while len(ticker) < 7:
        ticker = ticker + ' '
    print ticker
    name = ticker + name
    if len(name) > 19:
        name = name[:18] + "-"
    while len(name) < 25:
        name += ' '
    return name

# Create your views here.
def current_data(request):
    header = ['Year',]
    data = [header,]
    dates = [(today - datetime.timedelta(num)).strftime('%Y-%m-%d') for num in range(8, 1, -1)]
    i = 0

    while i < len(dates):
        dateline = [dates[i][5:],]
        j = 0
        while j < len(charted_industries.keys()):     # do all industry logic here
            key = charted_industries.keys()[j]
            if key not in header:
                header.append(key)
            entry = charted_industries[key].data
            for item in entry:
                if item[0] == dates[i]:
                    dateline.append(item[1])
            j += 1
        k = 0
        while k < len(charted_companies.keys()):
            key = charted_companies.keys()[k]
            if key not in header:
                header.append(key)
                header.append(key + " Predicted")

        data.append(dateline)
        i += 1
    jdata = json.dumps(data)

    response = HttpResponse(jdata)
    return response


def linegraph(request):

    cos = [company for company in Company.objects.all()]
    for co in cos:
        names = [ind.name for ind in master_industries]
        print names
        if str(co.industry) not in names:
            idstry = Industry()
            idstry.name = co.industry
            idstry.companies.append(co)
            master_industries.append(idstry)
    html = render(request, 'linegraph.html', {
        'industries':master_industries,
    })

    return html


def toggle(request):
    indus = request.GET['ind']
    com = request.GET['co']
    dates = [today-datetime.timedelta(num) for num in range(8, 1, -1)]
    if indus is not None:
        if indus in charted_industries.keys():
            print indus
            ind_obj = charted_industries[indus]
            ind_obj.toggled = False
            ind_obj.data = []
            del charted_industries[indus]
        else:
            indus_object = industry_for_name(indus)
            datum = []
            for date in dates:
                #add industry average performance for the date
                count = 0
                avg_performance = 0.
                for company in Company.objects.filter(industry=indus):
                    #print company
                    for price in Price.objects.filter(company=company, date=date):
                        #print price
                        avg_performance += float(price.price)
                        count += 1
                avg_performance = avg_performance / count
                datum.append([date.strftime('%Y-%m-%d'), avg_performance])
            indus_object.data = datum
            indus_object.toggled = True
            charted_industries[str(indus)]=indus_object
        return HttpResponse('')

    if com is not None:
        if com in charted_companies.keys():
            print com
            datum = []
            args = {}
            args['ticker'] = com
            company = Company.objects.get(ticker=com)
            for date in dates:
                datum.append(evaluate.evaluate(date=date,company=args))
        return HttpResponse('')




    return HttpResponseBadRequest

def search(request):
    query = request.GET['q']
    print query
    cos = Company.objects.filter(name__istartswith=query)
    cos = cos[:10]
    names = ["%s" % (format_name_for_display(co.ticker,co.name)) for co in cos]
    jdata = json.dumps(names)
    print jdata
    return HttpResponse(jdata)















