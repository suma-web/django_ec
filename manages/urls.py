from django.contrib import admin
from django.urls import path, include
from . import views


app_name = "manages"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("products/orders/", views.order_list, name="order_list"),
    path("products/orders/<int:order_id>/", views.order_detail, name="order_detail"),
]