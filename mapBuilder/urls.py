from django.urls import path
from mapBuilder.views import RoomListView
from . import views

app_name = 'mapBuilder'
urlpatterns = [
    # ex: /polls/
    path('', views.Index.as_view(), name='index'),
    path('', RoomListView.as_view(), name='room-list'),
    path('<slug:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
]
