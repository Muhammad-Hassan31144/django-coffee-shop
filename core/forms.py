from django import forms
from .models import Order, User

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'items_ordered', 'total_price']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'items_ordered': forms.Textarea(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }


