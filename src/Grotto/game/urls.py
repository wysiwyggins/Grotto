from django.urls import path

from . import views

app_name = "game"
urlpatterns = [
    path("enter/", views.EnterGrottoView.as_view(), name="enter"),
    # path("move/<slug:colorSlug>/", views.MoveView.as_view(), name="move"),
    # path("fire/<slug:colorSlug>/", views.FireArrowView.as_view(), name="fire"),
    path("become/<int:character_pk>/", views.BecomeCharacterView.as_view(), name="become"),
    # path("itemActions/use/<int:item_pk>/", views.UseItemView.as_view(), name="use"),
    # path("itemActions/take/<int:item_pk>/", views.TakeItemView.as_view(), name="take"),
    # path("itemActions/place/<int:item_pk>/", views.PlaceItemView.as_view(), name="place"),
    # path("itemActions/drop/<int:item_pk>/", views.DropItemView.as_view(), name="drop"),
    # path("itemActions/view/<int:item_pk>/", views.ViewItemView.as_view(), name="view"),
]
