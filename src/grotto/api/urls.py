from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from grotto.api import views

schema_view = get_schema_view(
    openapi.Info(
        title="Grotto API",
        default_version="v1",
        description="Idk",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register("rooms", views.RoomViewSet, basename="room")
router.register("characters", views.CharacterViewSet, basename="character")
router.register("items", views.ItemViewSet, basename="item")

urlpatterns = router.urls

urlpatterns += [
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

]
