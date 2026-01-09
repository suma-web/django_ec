def cart_item_count(request):
    cart = request.session.get("cart", {})
    total_quantity = sum(item.get("quantity", 0) for item in cart.values())
    
    return {"cart_item_count": total_quantity}