from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {}
    return render(request, '/guild/', context)

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['now'] = timezone.now()
    return context

def post(self, request):
    generateCharacter()
    return redirect('.') # points the user right back where they came from
