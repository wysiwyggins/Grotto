from django.urls import path

from . import views

app_name = 'mapBuilder'
urlpatterns = [
    # ex: /polls/
    path('', views.Index.as_view(), name='index'),
    path('<slug:pk>/', views.RoomDetail.as_view(), name='room_detail'),
]
