import os
import requests
from .models import Cart

def send_mailgun_message(to_email, subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxb9abe36b8e3d49a9bde83ecfc51667e7.mailgun.org/messages",
        auth=("api", os.environ["MAILGUN_API_KEY"]),
        data={
            "from": "Mailgun Sandbox <postmaster@sandboxb9abe36b8e3d49a9bde83ecfc51667e7.mailgun.org>",
            "to": to_email,
            "subject": subject,
            "text": text,
        }
    )

def build_order_email_text(order):
    lines = []
    lines.append("ご購入ありがとうございます。\n")
    lines.append(f"注文番号: {order.id}\n")
    lines.append("【ご注文内容】")

    total = 0

    for item in order.items.all():
        subtotal = item.product_price * item.quantity
        total += subtotal

        lines.append(
            f"- {item.product_name}\n"
            f"  単価: ¥{item.product_price:,}\n"
            f"  数量: {item.quantity}\n"
            f"  小計: ¥{subtotal:,}\n"
        )

    lines.append("----------------------")
    lines.append(f"合計金額: ¥{total:,}")
    lines.append("\nまたのご利用をお待ちしております。")

    return "\n".join(lines)

def get_cart(request):
    cart_id = request.session.get("cart_id")
    if cart_id:
        try:
            return Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            pass

    cart = Cart.objects.create(
        user=request.user if request.user.is_authenticated else None
    )
    request.session["cart_id"] = cart.id
    return cart