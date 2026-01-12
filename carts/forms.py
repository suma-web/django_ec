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
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "address2": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-select"}),
            "state": forms.Select(attrs={"class": "form-select"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control"}),
            "code_name": forms.TextInput(attrs={"class": "form-control"}),
            "code_number": forms.TextInput(attrs={"class": "form-control"}),
            "code_expiration": forms.TextInput(attrs={"class": "form-control"}),
            "code_cvv": forms.TextInput(attrs={"class": "form-control"}),
        }