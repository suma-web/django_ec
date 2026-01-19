from django.urls import path
from . import views

app_name = "carts"

urlpatterns = [
    path("", views.cart_view, name="cart_view"),
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="order_list"), 
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("promo/", views.apply_promo_code, name="apply_promo_code"),
    path("apply-promo/",views.apply_promotion_code,name="apply_promo"),
]