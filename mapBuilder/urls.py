from django.urls import path

from . import views

app_name = 'mapBuilder'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('<slug:slug>/', views.RoomDetail.as_view(), name='room_detail'),
]