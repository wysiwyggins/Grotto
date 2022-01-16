from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from Grotto.api import views

schema_view = get_schema_view(
    openapi.Info(
        title="Grotto API",
        default_version="v1",
        description="Idk",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(
        r"swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),

    path("map/", include("mapBuilder.api.urls", namespace="map-api")),
    path("tableau/", views.TableauAPIView.as_view(), name="tableau"),
    path("enter/", views.EnterAPIView.as_view()),
    path("move/<int:pk>/", views.MoveAPIView.as_view()),
    path("fire/<int:pk>/", views.FireArrowAPIView.as_view()),
    path("become/<int:pk>/", views.BecomeCharacterAPIView.as_view()),
    path("itemActions/use/<int:pk>/", views.UseItemAPIView.as_view()),
    path("itemActions/take/<int:pk>/", views.TakeItemAPIView.as_view()),
    path("itemActions/place/<int:pk>/", views.PlaceItemAPIView.as_view()),
    path("itemActions/drop/<int:pk>/", views.DropItemAPIView.as_view()),
    path("itemActions/view/<int:pk>/", views.ViewItemAPIView.as_view()),
]
