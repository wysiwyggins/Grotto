from random import sample

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from characterBuilder.models import Character, Visit
from Grotto.views import ActionMixin, LoginRequiredMixin
from mapBuilder.models import Room

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
    actions = [
       """  {
            "url": "#",
            "text": "real action 1",
        },
        {
            "url": "#",
            "text": "real action 2",
        },
        {
            "url": "#",
            "text": "real action 3",
        }, """
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deduped_visits = []
        visitors = []
        visits = Visit.objects.filter(room=self.object).order_by("stamp_date")
        for visit in visits:
            if visit.character not in visitors:
                deduped_visits.append(visit)
                visitors.append(visit.character)
        context.update(
            {
                "visits": deduped_visits,
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
