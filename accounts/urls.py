from django.urls import path
from .views import preferences

urlpatterns = [
    path("preferences/", preferences, name = "preferences"),
]