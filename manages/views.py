from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .forms import ProductForm
from django.views.decorators.http import require_POST
from products.models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, "manages/product_list.html", {
        "products": products
    })

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

@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("manages:product_list")