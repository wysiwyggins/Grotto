from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'mapBuilder/index.html', context)
    return HttpResponse(template.render(context, request))
