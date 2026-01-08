from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import CartItem
from .cart import Cart
from .services import get_or_create_cart

def cart_view(request):
    cart = Cart(request)
    context = {
        "cart": cart,
        "cart_total": cart.get_total_price(),
        "cart_item_count": cart.get_total_quantity(),
    }
    return render(request, "carts/cart_view.html", context)

def cart_add(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"price_at_add": product.price}
    )

    if not created:
        item.quantity += 1

    item.save()
    return redirect("carts:cart_view")

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("carts:cart_view")