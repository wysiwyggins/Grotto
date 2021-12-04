
from django.urls import path
from rest_framework import routers

from mapBuilder.api import views

app_name = "map-api"

urlpatterns = [
    path("room/<int:pk>/", views.RoomView.as_view(), name="room")
]
