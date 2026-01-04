from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "manages"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="manages/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
]