from django.shortcuts import render, get_object_or_404 
from .models import Product

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.exclude(pk=pk).order_by('-created_at')[:4]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })
