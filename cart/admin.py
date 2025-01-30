from django.contrib import admin
from .models import Cart, CartItem, Favourite,Coupon

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favourite)
admin.site.register(Coupon)
