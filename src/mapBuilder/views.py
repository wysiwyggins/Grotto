from random import sample
from datetime import timedelta

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from characterBuilder.models import Character, Visit
from Grotto.views import ActionMixin, LoginRequiredMixin
from mapBuilder.models import Room
from itemBuilder.enum import ItemType

# import function to run
from mapBuilder.room_generator import generateRoom


class Index(LoginRequiredMixin, ListView):
    template_name = "mapBuilder/index.html"
    model = Room
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

    def post(self, request):
        generateRoom()
        return redirect(".")  # points the user right back where they came from


class PlayDetailView(LoginRequiredMixin, TemplateView):
    template_name = "mapBuilder/play.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "room_context": {
                    "user": {
                        "is_anonymous": self.request.user.is_anonymous,
                        "is_staff": self.request.user.is_staff,
                    }
                }
            }
        )
        return context


class RoomDetailView(DetailView):
    model = Room
    template_name = "mapBuilder/room.html"
    query_pk_and_slug = True
    slug_url_kwarg = "colorSlug"
    slug_field = "colorSlug"
    sanctity_adjectives = ("Cursed", "Mundane", "Sacred")
    cleanliness_adjectives = ("Profane", "Dirty", "Clean")
    actions = []

    def _room_level(self, item_type):
        room = self.object
        # check items in room
        _item = room.items.filter(
            abstract_item__itemType=item_type, active__isnull=False
        )

        active_item_count = sum([1 for candle in _item if candle.is_active])
        # active_item_count = 1
        if active_item_count > 0:
            return 2
        # check characters in room
        for character in room.occupants.all():
            # see if character has a candle
            _item = character.inventory.filter(
                abstract_item__itemType=item_type, active__isnull=False
            )
            active_item_count = sum([1 for candle in _item if candle.is_active])
            if active_item_count > 0:
                return 1
        return 0

    def get_room_level(self, descriptor="illumination"):
        room = self.object
        if descriptor == "cleanliness":
            return room.cleanliness
        if descriptor == "illumination":
            return self._room_level(ItemType.CANDLE)
        if descriptor == "sanctity":
            if room.is_cursed:
                return 0
            if self._room_level(ItemType.INCENSE) == 2:
                return 2
            return 1

    def get_room_adjective(self, descriptor):
        _level = self.get_room_level(descriptor)
        adjectives = getattr(self, f"{descriptor}_adjectives")
        try:
            return adjectives[_level]
        except IndexError:
            return "what?"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "visits": self.object.visits,
                "illumination_level": self.get_room_level("illumination"),
                "sanctity_adjective": self.get_room_adjective("sanctity"),
                "cleanliness_adjective": self.get_room_adjective("cleanliness"),
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CenotaphView(DetailView):
    model = Room
    template_name = "mapBuilder/room.html"
    query_pk_and_slug = True
    slug_url_kwarg = "colorSlug"
    slug_field = "colorSlug"
    template_name = "mapBuilder/cenotaph.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        try:
            return obj.cenotaph
        except ObjectDoesNotExist:
            raise Http404("No cenotaph here")
