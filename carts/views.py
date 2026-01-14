from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages
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


def checkout(request):
    if request.method != "POST":
        return redirect("carts:cart_view")

    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    if not cart_items.exists():
        messages.error(request, "カートが空です")
        return redirect("products:product_list")

    # Order 作成
    order = Order.objects.create(
        first_name=request.POST["firstName"],
        last_name=request.POST["lastName"],
        username=request.POST["username"],
        email=request.POST.get("email", ""),
        address=request.POST["address"],
        address2=request.POST.get("address2", ""),
        country=request.POST["country"],
        state=request.POST["state"],
        zip_code=request.POST["zip"],
        card_name=request.POST["cc-name"],
        card_number=request.POST["cc-number"],
        card_expiration=request.POST["cc-expiration"],
        card_cvv=request.POST["cc-cvv"],
        total_price=sum(item.total_price for item in cart_items),
    )

    # OrderItem 作成
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.price_at_add,
        )

    # カートを空にする
    cart_items.delete()

    messages.success(request, "購入ありがとうございます")
    return redirect("products:product_list")