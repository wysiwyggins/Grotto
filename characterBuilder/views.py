from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'characterBuilder/index.html', context)
    return HttpResponse(template.render(context, request))
