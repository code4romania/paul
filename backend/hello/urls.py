from django.urls import path

from . import views


app_name = "hello"
urlpatterns = [
    path("", views.home, name="homepage"),
    path("health/", views.health, name="health"),
]
