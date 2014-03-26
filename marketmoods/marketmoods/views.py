import datetime

from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello World")


def current_datetime(request):
    now = datetime.datetime.now()
    #t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    #html = t.render(Context({'current_date': now}))
    #return HttpResponse(html)
    return render(request, 'base.html', {
        'current_date': now,
    })


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except Exception, e:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    #html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset,dt)
    #return HttpResponse(html)
    return render(request)


def home(request):
    return render(request, 'home.html')