from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Character

# Create your views here.

class Index(LoginRequiredMixin, ListView):
    template_name = 'guild.html'
    model = Character
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def post(self, request):
        generateCharacter()
        return redirect('.') # points the user right back where they came from


class CharacterDetailView(LoginRequiredMixin, DetailView):
    model = Character
    template_name = 'characterBuilder/character.html'
    query_pk_and_slug = True
