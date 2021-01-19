from django.urls import path

from . import views

app_name = 'characterBuilder'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index')
]