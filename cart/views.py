from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .models import Product, Cart, CartItem, Favourite
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin



class AddToCartView(LoginRequiredMixin, View):
    def get_cart(self, request):
        if not request.session.session_key:
            request.session.create()
        
        try:
            # Try to get the cart based on the user
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            # If no cart for the user, try to get it based on the session
            try:
                cart = Cart.objects.get(cart_id=request.session.session_key)
            except Cart.DoesNotExist:
                # If no cart for the session, create a new cart
                cart = Cart.objects.create(cart_id=request.session.session_key, user=request.user)
        
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
        product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart(request)
        self.get_cart_item(product, cart)
        return redirect('cart')

class RemoveFromCartView(LoginRequiredMixin, View):
    def get_cart(self, request):
        if not request.session.session_key:
            request.session.create()
        
        try:
            return Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Cart.objects.get(cart_id=request.session.session_key)

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

class RemoveCartView(LoginRequiredMixin, View):
    def get_cart(self, request):
        if not request.session.session_key:
            request.session.create()
        
        try:
            return Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Cart.objects.get(cart_id=request.session.session_key)

    def post(self, request, product_id):
        cart = self.get_cart(request)
        if not cart:
            return redirect('cart')
        
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
        return redirect('cart')

class CartView(LoginRequiredMixin, View):
    def get_cart(self, request):
        if not request.session.session_key:
            request.session.create()
        
        try:
            return Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Cart.objects.get(cart_id=request.session.session_key)

    def get(self, request, *args, **kwargs):
        total = 0
        quantity = 0
        cart_items = None
        shipping = 0
        grand_total = 0
        try:
            cart = self.get_cart(request)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            shipping = 75 if cart_items else 0  # Only add shipping if there are items
            grand_total = total + shipping
        except ObjectDoesNotExist:
            pass  # Ignore if the cart doesn't exist

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'shipping': shipping,
            'grand_total': grand_total,
        }
        return render(request, 'mainshop/cart/cart.html', context)


class AddFavouriteView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        fav, created = Favourite.objects.get_or_create(user=request.user, product=product)
        if created:
            messages.success(request, "Product added to favourite")
        else:
            messages.info(request, "Product is already in your favourites")
        
        return redirect('favourite_list')

class RemoveFromFavView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Favourite.objects.filter(user=request.user, product=product).delete()
        messages.success(request, "Product removed from favourite")
        return redirect('favourite_list')

class FavouriteView(LoginRequiredMixin, View):
    def get(self, request):
        favourites = Favourite.objects.filter(user=request.user)
        context = {
            'favourites': favourites,
        }
        return render(request, 'mainshop/favourite/favourite.html', context)
