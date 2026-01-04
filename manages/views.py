from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .forms import ProductForm
from .auth import basic_auth_required


@basic_auth_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "manages/product_list.html", {
        "products": products
    })