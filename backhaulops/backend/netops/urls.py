
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("apps.core.urls")),
    #path("api/telemetry", include("apps.telemetry.urls"))
     path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("links.html", TemplateView.as_view(template_name="links.html"), name="links"),
    path("", TemplateView.as_view(template_name="login.html"), name="home"),

]
