from django.shortcuts import redirect
from django.views import View
from .models import Product, Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from django.http import Http404
from django.shortcuts import get_object_or_404

class AddToCartView(View):
    def get_cart(self, request):
        try:
            cart = Cart.objects.get(cart_id=request.session.session_key)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=request.session.session_key)
        return cart

    def get_cart_item(self, product, cart):
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
        return cart_item

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        
        cart = self.get_cart(request)
        self.get_cart_item(product, cart)
        return redirect('cart')


class RemoveFromCartView(View):
    def get_cart(self, request):
        try:
            return Cart.objects.get(cart_id=request.session.session_key)
        except Cart.DoesNotExist:
            return None

    def post(self, request, product_id):
        cart = self.get_cart(request)
        if not cart:
            return redirect('cart')

        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect('cart')

class RemoveCartView(View):
    def get_cart(self,request):
        try:
            return Cart.objects.get(cart_id=request.session.session_key)
        except Cart.DoesNotExist:
            return None
        
    def post(self,request,product_id):
        cart = self.get_cart(request)
        if not cart:
            return redirect('cart')
        product = get_object_or_404(Product,id=product_id)
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.delete()
        return redirect('cart')
    

class CartView(View):
    def get_cart_id(self, request):
        # Ensure the session key exists
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key

    def get(self, request, *args, **kwargs):
        total = 0
        quantity = 0
        cart_items = None
        try:
            # Get the cart using the session key
            cart = Cart.objects.get(cart_id=self.get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            shipping = 75
            grand_total = total + shipping 
        except ObjectDoesNotExist:
            pass  # Ignore if the cart doesn't exist

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'shipping' : shipping,
            'grand_total' : grand_total,  
        }
        return render(request, 'mainshop/cart/cart.html', context)













