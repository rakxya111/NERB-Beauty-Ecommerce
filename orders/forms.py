from django import forms
from orders.models import Order, Payment

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','city','country','order_note']

