from django.http import Http404
from django.shortcuts import render
from django.views import generic
from .models import Room

# Create your views here.
from django.http import HttpResponse
# Create your views here.



def index(request):
    queryset = Room.objects.filter(status=1).order_by('-created_on')
    template_name = 'mapBuilder/index.html'

class RoomDetail(generic.DetailView):
    model = Room
    template_name = 'room.html'