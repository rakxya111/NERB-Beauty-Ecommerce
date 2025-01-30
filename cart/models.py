from django.db import models
from mainshop.models import Product
from django.conf import settings
from django.utils import timezone


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user) if self.user else self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name




class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)  # Discount amount
    is_percentage = models.BooleanField(default=False)  # If True, treat as percentage
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Optional minimum order value
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        """Check if coupon is valid"""
        return self.is_active and (not self.expiry_date or self.expiry_date > timezone.now())

    def __str__(self):
        return self.code
