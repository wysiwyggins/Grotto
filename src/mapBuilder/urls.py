from django.urls import path
from django.views.generic import TemplateView

from mapBuilder.views import Index

from . import views

app_name = "mapBuilder"
urlpatterns = [
    # ex: /polls/
    path("", views.Index.as_view(), name="index"),
    path("new/", views.NewRoomDetailView.as_view()),
    path("<slug:colorSlug>/", views.RoomDetailView.as_view(), name="room"),
    path("gui/<slug:colorSlug>/", views.GraphicalRoomView.as_view(), name="gui"),
]
