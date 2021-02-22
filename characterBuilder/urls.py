from django.urls import path

from . import views

app_name = 'characterBuilder'
urlpatterns = [
    # ex: /polls/
    path('', views.Index.as_view(), name='index'),
    path('character/<int:pk>/', views.CharacterDetailView.as_view(), name='character'),
    path('test/', views.CharacterTestView.as_view(), name='character-test'),
    path('write-test/', views.CharacterTestCreateView.as_view(), name='character-test-create'),
    path('new-character/', views.NewCharacterView.as_view(), name="new-character"),
]
