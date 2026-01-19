from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages
from django.conf import settings
from django.db import transaction
from .models import CartItem, Order, OrderItem, PromotionCode
from .services import get_or_create_cart
from django.conf import settings
from .utils import send_mailgun_message, build_order_email_text, get_cart
from django.template.loader import render_to_string
from .auth import basic_auth_required
from django.views.decorators.http import require_POST


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
    
    with transaction.atomic():
        order = Order.objects.create(
            first_name=request.POST["firstName"],
            last_name=request.POST["lastName"],
            username=request.POST["username"],
            email=request.POST["email"],
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
            promotion=cart.promotion_code,
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                product_price=item.price_at_add,
                quantity=item.quantity,
            )

        if cart.promotion_code:
            cart.promotion_code.is_used = True
            cart.promotion_code.save()
            
        cart.items.all().delete()
        cart.promotion = None
        cart.save()
    
    send_mailgun_message(
        to_email=request.POST.get("email"),
        subject="ご購入ありがとうございます",
        text=build_order_email_text(order)
    )

    messages.success(request, "購入ありがとうございます")
    return redirect("products:list")

@require_POST
def apply_promo_code(request):
    cart = get_cart(request)
    code = request.POST.get("promo_code", "").strip().upper()

    try:
        promo = PromotionCode.objects.get(
            code=code,
            is_used=False
        )
    except PromotionCode.DoesNotExist:
        messages.error(request, "無効なプロモーションコードです")
        return redirect("carts:cart_view")

    cart.promotion_code = promo
    cart.save()

    messages.success(
        request,
        f"¥{promo.discount_amount} の割引が適用されました"
    )
    return redirect("carts:cart_view")


@basic_auth_required
def order_list(request):
    orders = Order.objects.order_by("-created_at")
    return render(request, "carts/order_list.html", {
        "orders": orders
    })

@basic_auth_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    return render(request, "carts/order_detail.html", {
        "order": order,
        "items": items
    })

