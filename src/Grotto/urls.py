"""Grotto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from Grotto.views import RegisterView, TermsAcceptView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("rooms/", include("mapBuilder.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("guild/", include("characterBuilder.urls")),
    path("game/", include("Grotto.game.urls")),
    path("api/v1/", include("Grotto.api.urls")),
    path("terms/", TermsAcceptView.as_view(), name="terms"),
    path(
        "privacy/",
        TemplateView.as_view(template_name="static_pages/privacy.html"),
        name="privacy",
    ),
    path(
        "agreement/",
        TemplateView.as_view(template_name="static_pages/agreement.html"),
        name="agreement",
    ),
    path(
        "reporting/",
        TemplateView.as_view(template_name="static_pages/reporting.html"),
        name="reporting",
    ),
]
