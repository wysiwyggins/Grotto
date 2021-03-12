
from django.urls import path
from . import views


app_name = 'game'
urlpatterns = [
    path('enter/', views.EnterGrottoView.as_view(), name="enter"),
    path('move/<slug:colorSlug>/', views.MoveView.as_view(), name="move"),
    path('fire/<slug:colorSlug>/', views.FireArrowView.as_view(), name="fire"),
]
