from django.urls import path
from . import views

app_name = "accounts" 

urlpatterns = [
    path("login/", views.user_login, name="user_login"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("logout/", views.logout_view, name="logout"),
]
