# cart/context_processors.py
from cart.models import Cart, CartItem

def cart_item_count(request):
    item_count = 0
    if 'admin' in request.path:
        return {}

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            item_count = sum(cart_item.quantity for cart_item in cart_items)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        try:
            cart = Cart.objects.filter(cart_id=session_key).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart)
                item_count = sum(cart_item.quantity for cart_item in cart_items)
        except Cart.DoesNotExist:
            item_count = 0

    return {'item_count': item_count}
