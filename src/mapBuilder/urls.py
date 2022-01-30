from django.urls import path
from django.views.generic import TemplateView

from mapBuilder.views import Index

from . import views

app_name = "mapBuilder"
urlpatterns = [
    # ex: /polls/
    path("", views.Index.as_view(), name="index"),
    path("play/", views.PlayDetailView.as_view(), name="play"),
    path("<slug:colorSlug>/", views.RoomDetailView.as_view(), name="room"),
    path("cenotaph/<slug:colorSlug>/", views.CenotaphView.as_view(), name="cenotaph"),
]
