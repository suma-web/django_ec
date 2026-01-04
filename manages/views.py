from django.shortcuts import render
from products.models import Product
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_staff_user)
def product_list(request):
    products = Product.objects.all()
    return render(request, "manages/product_list.html", {
        "products": products
    })

def product_create(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST["name"],
            price=request.POST["price"],
        )
        return redirect("manages:product_list")

    return render(request, "manages/product_create.html")

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("manages:product_list")

    return render(request, "manages/product_confirm_delete.html", {
        "product": product
    })