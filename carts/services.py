from .models import Cart

def get_or_create_cart(request):
    cart_id = request.session.get("cart_id")

    if cart_id:
        return Cart.objects.get(id=cart_id)

    cart = Cart.objects.create(
        user=request.user if request.user.is_authenticated else None
    )
    request.session["cart_id"] = cart.id
    return cart