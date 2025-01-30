from cart.models import Cart, CartItem, Favourite

# def counter(request):
#     item_count = 0
#     if 'admin' in request.path:
#         return {}

#     session_key = request.session.session_key
#     if session_key is None:  # ✅ Ensure session exists
#         request.session.create()
#         session_key = request.session.session_key

#     try:
#         cart = Cart.objects.filter(cart_id=session_key)
#         cart_items = CartItem.objects.filter(cart=cart[:1])  # ✅ Fix filtering
#         for cart_item in cart_items:
#             item_count += cart_item.quantity
#     except Cart.DoesNotExist:
#         item_count = 0

#     return dict(item_count=item_count)


def favourite_counter(request):
    fav_count = 0
    if 'admin' in request.path:
        return {}

    if request.user.is_authenticated:  # ✅ Check if the user is logged in
        fav_count = Favourite.objects.filter(user=request.user).count()

    return dict(fav_count=fav_count)
