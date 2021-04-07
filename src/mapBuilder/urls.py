from django.urls import path

from mapBuilder.views import Index

from . import views

app_name = "mapBuilder"
urlpatterns = [
    # ex: /polls/
    path("", views.Index.as_view(), name="index"),
    path("<slug:colorSlug>/", views.RoomDetailView.as_view(), name="room"),
]
