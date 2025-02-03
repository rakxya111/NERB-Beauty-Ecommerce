from django.shortcuts import redirect, render
from django.http import HttpResponse
from cart.models import  Coupon,CartItem
from orders.forms import OrderForm
import datetime
from django.contrib import messages
from orders.models import Order


def payments(request):
    return render(request,'mainshop/orders/payments.html')



def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(cart__user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    shipping = 75 if cart_count > 0 else 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        grand_total += (cart_item.product.price * cart_item.quantity)

    grand_total += shipping

    # Retrieve the coupon code from session
    coupon_code = request.session.get('coupon_code', None)
    discount_amount = 0
    applied_coupon = None

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            
            # Check coupon validity
            if coupon.expiry_date and coupon.expiry_date < datetime.date.today():
                messages.error(request, "Coupon has expired.")
                request.session.pop('coupon_code', None)  # Remove expired coupon
            elif total < coupon.min_order_value:
                messages.error(request, f"Minimum order value should be {coupon.min_order_value} to use this coupon.")
                request.session.pop('coupon_code', None)
            else:
                # Apply discount
                if coupon.is_percentage:
                    discount_amount = (total * coupon.discount) / 100
                else:
                    discount_amount = coupon.discount
                
                discount_amount = min(discount_amount, total)  # Prevent negative total
                grand_total -= discount_amount
                applied_coupon = coupon
        except Coupon.DoesNotExist:
            request.session.pop('coupon_code', None)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.shipping_fee = shipping
            data.discount_amount = discount_amount  # Store discount amount
            data.coupon = applied_coupon  # Save applied coupon if any
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'shipping': shipping,
                'grand_total': grand_total,
                'discount_amount': discount_amount,
                'applied_coupon': applied_coupon,
            }

            messages.success(request, 'Order placed successfully!')
            return render(request, 'mainshop/orders/payments.html', context)

        else:
            messages.error(request, 'There was an issue with your order submission. Please try again.')
            return redirect('checkout')

