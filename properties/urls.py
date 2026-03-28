from django.urls import path
from properties import views

urlpatterns = [
path('', views.owner_signup, name = 'owner_signup'),
path('submit/', views.submit_property, name='submit_property'),
]