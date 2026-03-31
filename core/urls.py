from django.urls import path, include
from core import views
urlpatterns = [
    path('',views.home, name='home'),
    path('home/', views.home, name='home'),
    path("signup/", views.signup , name = "signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("ajax-reset-request/", views.request_password_reset, name="ajax_reset_request"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('api/properties/', views.load_more_properties, name='load_more_properties'),
]
