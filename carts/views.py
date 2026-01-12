from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .forms import CheckoutForm
from .models import CartItem, Order, OrderItem
from .services import get_or_create_cart


def cart_view(request):
    cart = get_or_create_cart(request)

    context = {
        "cart": cart,
        "cart_item_count": cart.items.count(),
        "cart_total": sum(
            item.price_at_add * item.quantity
            for item in cart.items.all()
        ),
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
    cart = get_or_create_cart(request)
    CartItem.objects.filter(
            cart=cart,
            product_id=product_id
        ).delete()
    return redirect("carts:cart_view")

def checkout_view(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    if not cart_items.exists():
        return redirect("carts:cart_view")

    total_price = sum(item.total_price for item in cart_items)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.total_price = total_price
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price_at_add,
                )

            cart_items.delete()

            return redirect("carts:checkout_complete")

    else:
        form = CheckoutForm()

    return render(request, "carts/checkout.html", {
        "form": form,
        "cart_items": cart_items,
        "cart_total": total_price,
    })