from django.urls import path
from core import views
urlpatterns = [
    path('', views.home, name='home'),
    path("signup/", views.signup , name = "signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("ajax-reset-request/", views.request_password_reset, name="ajax_reset_request"),


]
