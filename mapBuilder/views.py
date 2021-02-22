from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from Grotto.views import ActionMixin

from .models import Room
# import function to run
from .room_generator import generateRoom


class Index(LoginRequiredMixin, ListView):
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


class RoomDetailView(LoginRequiredMixin, ActionMixin, DetailView):
    model = Room
    template_name = 'mapBuilder/room.html'
    query_pk_and_slug = True
    slug_url_kwarg = 'colorSlug'
    slug_field = 'colorSlug'
    actions = [{
        "url": "#",
        "text": "real action 1",
    }, {
        "url": "#",
        "text": "real action 2",
    }, {
        "url": "#",
        "text": "real action 3",
    }, ]

