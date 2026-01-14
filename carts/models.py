from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_add = models.IntegerField()

    @property
    def total_price(self):
        return self.price_at_add * self.quantity

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True)

    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    card_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=30)
    card_expiration = models.CharField(max_length=10)
    card_cvv = models.CharField(max_length=10)

    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.IntegerField()
    quantity = models.IntegerField()

    @property
    def total_price(self):
        return self.product_price * self.quantity