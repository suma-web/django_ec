from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .forms import ProductForm
from django.views.decorators.http import require_POST
from products.models import Product
from .auth import basic_auth_required
from carts.models import Order


@basic_auth_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "manages/product_list.html", {
        "products": products
    })

@basic_auth_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("manages:product_list")
    else:
        form = ProductForm()

    return render(request, "manages/product_form.html", {
        "form": form
    })

@basic_auth_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("manages:product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "manages/product_form.html", {
        "form": form,
        "product": product
    })

@basic_auth_required
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("manages:product_list")


@basic_auth_required
def order_list(request):
    orders = Order.objects.order_by("-created_at")
    return render(request, "manages/orders/order_list.html", {
        "orders": orders
    })

@basic_auth_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    return render(request, "manages/orders/order_detail.html", {
        "order": order,
        "items": items
    })