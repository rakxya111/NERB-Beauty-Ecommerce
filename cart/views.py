from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .models import Coupon, Product, Cart, CartItem, Favourite
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse



# Helper function to get session-based cart
def get_session_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart_id = request.session.get('cart_id')
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)
    return cart

# Function to transfer items from session cart to user cart
def transfer_cart_items_to_user_cart(request, user_cart):
    session_cart = get_session_cart(request)
    if session_cart:
        for session_cart_item in CartItem.objects.filter(cart=session_cart):
            # Transfer session cart items to the user's cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=session_cart_item.product,
                defaults={'quantity': session_cart_item.quantity}
            )
            if not created:
                cart_item.quantity += session_cart_item.quantity
                cart_item.save()
        
        # After transferring items, clear the session cart
        session_cart.cartitem_set.all().delete()
        request.session['cart_id'] = None  # Clear session cart ID

# AddToCartView - only accessible for authenticated users
@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def get_cart(self, request):
        if request.user.is_authenticated:
            # For logged-in users, use the user-based cart
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            # For anonymous users, use session-based cart
            cart = get_session_cart(request)
        return cart

    def get_cart_item(self, product, cart):
        cart_item, created = CartItem.objects.get_or_create(
            product=product, cart=cart, defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return cart_item

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart(request)
        self.get_cart_item(product, cart)
        return redirect(reverse('cart'))

# RemoveFromCartView - to remove product from cart
@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    def get_cart(self, request):
        cart = None
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = get_session_cart(request)
        return cart

    def post(self, request, product_id):
        cart = self.get_cart(request)
        if not cart:
            return redirect(reverse('cart'))

        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.filter(product=product, cart=cart).first()

        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        return redirect(reverse('cart'))

# RemoveCartView - to clear entire cart
@method_decorator(login_required, name='dispatch')
class RemoveCartView(View):
    def get_cart(self, request):
        cart = None
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = get_session_cart(request)
        return cart

    def post(self, request, product_id):
        cart = self.get_cart(request)
        if not cart:
            return redirect(reverse('cart'))

        product = get_object_or_404(Product, id=product_id)
        CartItem.objects.filter(product=product, cart=cart).delete()
        return redirect(reverse('cart'))

# CartView - to show the cart items
@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = get_session_cart(request)
        return cart

    def get(self, request, *args, **kwargs):
        total = 0
        quantity = 0
        cart_items = None
        shipping = 0
        grand_total = 0
        coupon_code = request.session.get('coupon_code', None)
        applied_coupon = None
        discount_amount = 0

        cart = self.get_cart(request)
        if cart:
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            shipping = 75 if cart_items else 0
            grand_total = total + shipping

         # Apply coupon discount if valid
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    if coupon.is_valid() and total >= coupon.min_order_value:
                        if coupon.is_percentage:
                            discount_amount = (total * coupon.discount) / 100
                        else:
                            discount_amount = coupon.discount
                        grand_total -= discount_amount
                        applied_coupon = coupon
                    else:
                        request.session.pop('coupon_code', None)  # Remove invalid coupon
                except Coupon.DoesNotExist:
                    request.session.pop('coupon_code', None)

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'shipping': shipping,
            'grand_total': grand_total,
            'discount_amount': discount_amount,
            'applied_coupon': applied_coupon,
        }
        return render(request, 'mainshop/cart/cart.html', context)

    def post(self, request, *args, **kwargs):
        """Handles coupon application"""
        coupon_code = request.POST.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid():
                    request.session['coupon_code'] = coupon_code
                    messages.success(request, "Coupon applied successfully!")
                else:
                    messages.error(request, "Coupon is expired or invalid.")
            except Coupon.DoesNotExist:
                messages.error(request, "Invalid coupon code.")

        return redirect('cart')  # Redirect to cart view



@method_decorator(login_required, name='dispatch')
class AddFavouriteView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        fav, created = Favourite.objects.get_or_create(user=request.user, product=product)
        if created:
            messages.success(request, "Product added to favourite")
        else:
            messages.info(request, "Product is already in your favourites")

        return redirect('favourite_list')


@method_decorator(login_required, name='dispatch')
class RemoveFromFavView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Favourite.objects.filter(user=request.user, product=product).delete()
        messages.success(request, "Product removed from favourite")
        return redirect('favourite_list')



class FavouriteView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to view favourites.")
            return redirect('login')  # Redirect to login page
        
        favourites = Favourite.objects.filter(user=request.user)
        context = {
            'favourites': favourites,
        }
        return render(request, 'mainshop/favourite/favourite.html', context)



@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get_cart(self, request):
        """Returns the user's cart or session-based cart if implemented"""
        if request.user.is_authenticated:
            return Cart.objects.filter(user=request.user).first()
        return get_session_cart(request)  # Ensure this function is defined elsewhere

    def get(self, request, *args, **kwargs):
        total = 0
        quantity = 0
        shipping = 0
        grand_total = 0
        coupon_code = request.session.get('coupon_code', None)
        applied_coupon = None
        discount_amount = 0

        cart = self.get_cart(request)
        cart_items = None

        if cart:
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for item in cart_items:
                total += item.product.price * item.quantity
                quantity += item.quantity

            shipping = 75 if cart_items else 0
            grand_total = total + shipping
        
        # Apply coupon discount if valid
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    if coupon.is_valid() and total >= coupon.min_order_value:
                        if coupon.is_percentage:
                            discount_amount = (total * coupon.discount) / 100
                        else:
                            discount_amount = coupon.discount
                        grand_total -= discount_amount
                        applied_coupon = coupon
                    else:
                        request.session.pop('coupon_code', None)  # Remove invalid coupon
                except Coupon.DoesNotExist:
                    request.session.pop('coupon_code', None)

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'shipping': shipping,
            'grand_total': grand_total,
            'discount_amount': discount_amount,
            'applied_coupon': applied_coupon,
        }
        return render(request, 'mainshop/cart/checkout.html', context)



