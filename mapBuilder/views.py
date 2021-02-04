from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic
from .models import Room

# import function to run
from .room_generator import generateRoom

# Create your views here.
from django.http import HttpResponse
# Create your views here.


class Index(generic.ListView):
    queryset = Room.objects.filter(status=1).order_by('-pub_date')
    template_name = 'mapBuilder/index.html'

    def post(self, request):
        generateRoom()
        return redirect('.') # points the user right back where they came from

class RoomList(generic.ListView):
    queryset = Room.objects.filter(status=1).order_by('-pub_date')
    template_name = 'mapBuilder/index.html'

class RoomDetail(generic.DetailView):
    model = Room
    template_name = 'mapBuilder/room.html'