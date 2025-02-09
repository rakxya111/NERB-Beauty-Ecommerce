from django.shortcuts import redirect, render
from django.http import HttpResponse
from cart.models import  Coupon,CartItem
from orders.forms import OrderForm
import datetime
from django.contrib import messages
from orders.models import Order, OrderProduct, Payment
import uuid
from django.contrib.auth.decorators import login_required




@login_required
def payments(request, order_number):
    user = request.user
    try:
        # Try to get the order by order_number
        order = Order.objects.get(user=user, order_number=order_number, is_ordered=False)
    except Order.DoesNotExist:
        # If the order does not exist, return an error message
        messages.error(request, "Order not found or already placed.")
        return redirect('product-list')  # Redirect to the store page or another relevant page

    cart_items = CartItem.objects.filter(cart__user=user)

    total = 0
    grand_total = 0
    shipping = 75 if cart_items.count() > 0 else 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
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
            if coupon.expiry_date and coupon.expiry_date.date() < datetime.date.today():
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

    context = {
        'order': order,
        'cart_items': cart_items,
        'total': total,
        'shipping': shipping,
        'grand_total': grand_total,
        'discount_amount': discount_amount,
        'applied_coupon': applied_coupon,
    }

    if request.method == "POST":
        payment_method = request.POST.get('payment_method', 'Khalti')
        payment_id = str(uuid.uuid4().hex[:12]).upper()

        # Create payment record
        payment = Payment.objects.create(
            user=user,
            payment_id=payment_id,
            payment_method=payment_method,
            status="Completed"
        )

        # After payment, create OrderProduct and update the order
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                user=user,
                product=cart_item.product,
                quantity=cart_item.quantity,
                product_price=cart_item.product.price,
                ordered=True,
                payment=payment
            )

        # Mark order as complete and delete cart items
        order.is_ordered = True
        order.payment = payment
        order.save()
        cart_items.delete()

        messages.success(request, 'Payment confirmed! Your order has been placed.')
        return redirect('order_summary', order_number=order_number)
    else:
        messages.error(request, 'Something went wrong cannot place the order')
        return redirect('mainshop/orders/payments.html')


    return render(request, 'mainshop/orders/payments.html', context)





@login_required
def order_summary(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, user=request.user, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order=order)
        

        context = {
            'order': order,
            'ordered_products': ordered_products

            
        }
        return render(request, 'mainshop/orders/payment_confirmation.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('product-list')



@login_required
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
            if coupon.expiry_date and coupon.expiry_date.date() < datetime.date.today():
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

            # Instead of redirect, directly render the payments page
            return render(request, 'mainshop/orders/payments.html', context)

        else:
            messages.error(request, 'There was an issue with your order submission. Please try again.')
            return redirect('checkout')


