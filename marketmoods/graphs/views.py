from django.shortcuts import render

# Create your views here.
def linegraph(request):
    return render(request, 'linegraph.html')