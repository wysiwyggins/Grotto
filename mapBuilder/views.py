from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Room

# import function to run
from .room_generator import generateRoom

# Create your views here.
from django.http import HttpResponse
# Create your views here.


class Index(ListView):
    template_name = 'mapBuilder/index.html'
    model = Room
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def post(self, request):
        generateRoom()
        return redirect('.') # points the user right back where they came from


class RoomDetailView(DetailView):
    model = Room
    template_name = 'mapBuilder/room.html'