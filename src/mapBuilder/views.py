from random import sample
from datetime import timedelta

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.db.models import F

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


class RoomDetailView(LoginRequiredMixin, ActionMixin, DetailView):
    model = Room
    template_name = "mapBuilder/room.html"
    query_pk_and_slug = True
    slug_url_kwarg = "colorSlug"
    slug_field = "colorSlug"
    sanctity_adjectives = ("Cursed", "Mundane", "Sacred")
    cleanliness_adjectives = ("Profane", "Dirty", "Clean")
    actions = []

    def _room_level(self, item_type):
        room = self.request.character.room
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
        room = self.request.character.room
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
        deduped_visits = []
        visitors = []
        visits = (
            Visit.objects.filter(room=self.object)
            .exclude(stamp_date__lt=timezone.now() - timedelta(days=7))
            .order_by("-stamp_date")
        )
        for visit in visits:
            if visit.character not in visitors:
                deduped_visits.append(visit)
                visitors.append(visit.character)
        context.update(
            {
                "visits": deduped_visits,
                "illumination_level": self.get_room_level("illumination"),
                "sanctity_adjective": self.get_room_adjective("sanctity"),
                "cleanliness_adjective": self.get_room_adjective("cleanliness"),
            }
        )
        warnings = []
        for exit in self.object.exits.all():
            for npc in exit.npcs.all():
                warnings.append(npc.warning_text)
        context.update(
            {
                "warnings": sample(warnings, k=len(warnings)),
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        if request.character is None:
            if not request.user.is_superuser:
                # send them back to the guild hall
                return redirect("/guild/")
        else:
            if request.character.room.colorSlug != kwargs["colorSlug"]:
                return redirect(
                    reverse(
                        "mapBuilder:room",
                        kwargs={"colorSlug": request.character.room.colorSlug},
                    )
                )
        return super().get(request, *args, **kwargs)


class GraphicalRoomView(RoomDetailView):
    template_name = "cenotaph.html"
