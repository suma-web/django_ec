from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name", "last_name", "username", "email",
            "address", "address2", "country", "state", "zip_code",
            "card_name", "card_number", "card_expiration", "card_cvv",
        ]