from cart.models import Cart, CartItem, Favourite

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=request.session.session_key)
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count = 0
    return dict(item_count=item_count)

def favourite_counter(request):
    fav_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            fav = Favourite.objects.filter(user=request.user)
            fav_count = fav.count()
        except Favourite.DoesNotExist:
            fav_count = 0
    return dict(fav_count=fav_count)