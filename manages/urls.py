from django.contrib import admin
from django.urls import path, include
from . import views


app_name = "manages"

urlpatterns = [
    path("products/", views.product_list),
    path("products/create/", views.product_create),
    path("products/<int:pk>/edit/", views.product_edit),
    path("products/<int:pk>/delete/", views.product_delete),

]