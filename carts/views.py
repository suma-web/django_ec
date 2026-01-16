from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages
from django.conf import settings
from .models import CartItem, Order, OrderItem
from .services import get_or_create_cart
import requests
from django.conf import settings
from django.template.loader import render_to_string
from .auth import basic_auth_required

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
        return redirect("products:list")

    order = Order.objects.create(
        first_name=request.POST["firstName"],
        last_name=request.POST["lastName"],
        username=request.POST["username"],
        email=request.POST["email"],         # emailを明細を送るためにマスト
        address=request.POST["address"],
        address2=request.POST.get("address2", ""),
        country=request.POST["country"],
        state=request.POST["state"],
        zip_code=request.POST["zip"],
        card_name=request.POST["cc-name"],
        card_number=request.POST["cc-number"],
        card_expiration=request.POST["cc-expiration"],
        card_cvv=request.POST["cc-cvv"],
        total_price=cart.total_price,
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            product_price=item.product.price,
            quantity=item.quantity,
        )
    
    message = render_to_string(
        "emails/order_confirmation.txt",
        {
            "order": order,
            "items": order.items.all(),
        },
    )

    def send_order_mail(order, body):
        return requests.post(
            f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": f"Shop <mailgun@{settings.MAILGUN_DOMAIN}>",
                "to": [order.email],
                "subject": "ご購入ありがとうございます",
                "text": body,
            },
            timeout=10,
        )

    cart_items.delete()

    messages.success(request, "購入ありがとうございます")
    return redirect("products:list")

@basic_auth_required
def order_list(request):
    orders = Order.objects.order_by("-created_at")
    return render(request, "carts/order_list.html", {
        "orders": orders
    })


@basic_auth_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.orderitem_set.all()
    return render(request, "carts/order_detail.html", {
        "order": order,
        "items": items
    })