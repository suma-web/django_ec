from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart

def cart_view(request):
    cart = Cart(request)
    context = {
        "cart": cart,
        "cart_total": cart.get_total_price(),
        "cart_item_count": cart.get_total_quantity(),
    }
    return render(request, "carts/cart_view.html", context)

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get("quantity", 1))
    cart.add(product=product, quantity=quantity)

    return redirect("carts:cart_view")

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("carts:cart_view")