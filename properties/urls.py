from django.urls import path
from properties import views

urlpatterns = [
path('', views.property_home, name = 'property_home'),
]