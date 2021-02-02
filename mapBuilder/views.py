from django.http import Http404
from django.shortcuts import render
from django.views import generic
from .models import Room

# Create your views here.
from django.http import HttpResponse
# Create your views here.


class Index(generic.ListView):
    queryset = Room.objects.filter(status=1).order_by('-pub_date')
    template_name = 'mapBuilder/index.html'

    if request.method == 'POST' and 'generate_room' in request.POST:

        # import function to run
        from room_generator.py import generateRoom

        # call function
        generateRoom() 

        # return user to required page
        return HttpResponseRedirect(reverse(app_name:view_name)

class RoomList(generic.ListView):
    queryset = Room.objects.filter(status=1).order_by('-pub_date')
    template_name = 'mapBuilder/index.html'

class RoomDetail(generic.DetailView):
    model = Room
    template_name = 'mapBuilder/room.html'