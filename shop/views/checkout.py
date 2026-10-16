from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Customer, Order, OrderProduct, Cart
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from django.db import DataError

@login_required(login_url='/login')
def checkout(request):
    currentuser = request.user
    carts = Cart.objects.filter(user_id=currentuser.id)
    customer = Customer.objects.get(user_id=currentuser.id)
    myuser = User.objects.get(id=currentuser.id)

    total = 0
    qty = 0
    for cart in carts:
        total = total + cart.amount
        qty = qty + cart.qty
    
    discount = 10/100 * total
    if discount > 20000:
        discount = 20000

    grand_total = total - discount

    if request.method == "POST":
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        phone = request.POST.get('phone', '').strip()
        house_no = request.POST.get('house_no', '').strip()
        street = request.POST.get('street', '').strip()
        state = request.POST.get('state', '').strip()
        city = request.POST.get('city', '').strip()
        pin = request.POST.get('pin', '').strip()
        code = "OD-" + get_random_string(10).upper()

        form_data = {
            'firstname': firstname,
            'lastname': lastname,
            'phone': phone,
            'house_no': house_no,
            'street': street,
            'state': state,
            'city': city,
            'pin': pin,
        }

        # Form Validations
        if not phone.isdigit():
            messages.error(request, "Mobile number must contain digits only. Please fill it up again.")
            details = {
                'myuser': myuser,
                'customer': customer,
                'carts': carts,
                'qty': qty,
                'total': total,
                'discount': discount,
                'grand_total': grand_total,
                'form_data': form_data,
            }
            return render(request, 'checkout.html', details)

        if len(phone) > 15 or int(phone) > 9223372036854775807:
            messages.error(request, "Mobile number is out of range. Please fill it up again.")
            details = {
                'myuser': myuser,
                'customer': customer,
                'carts': carts,
                'qty': qty,
                'total': total,
                'discount': discount,
                'grand_total': grand_total,
                'form_data': form_data,
            }
            return render(request, 'checkout.html', details)

        if not pin.isdigit():
            messages.error(request, "PIN Code must contain digits only. Please fill it up again.")
            details = {
                'myuser': myuser,
                'customer': customer,
                'carts': carts,
                'qty': qty,
                'total': total,
                'discount': discount,
                'grand_total': grand_total,
                'form_data': form_data,
            }
            return render(request, 'checkout.html', details)

        if len(pin) > 6 or int(pin) > 2147483647:
            messages.error(request, "PIN Code is out of range. Please fill it up again.")
            details = {
                'myuser': myuser,
                'customer': customer,
                'carts': carts,
                'qty': qty,
                'total': total,
                'discount': discount,
                'grand_total': grand_total,
                'form_data': form_data,
            }
            return render(request, 'checkout.html', details)

        try:
            order = Order(
                user_id = currentuser.id,
                first_name = firstname,
                last_name = lastname,
                phone = int(phone),
                house_no = house_no,
                street = street,
                city = city,
                pin = int(pin),
                state = state,
                total = grand_total,
                code = code
            )
            order.save()
        except DataError:
            messages.error(request, "The entered details are out of range. Please fill it up again.")
            details = {
                'myuser': myuser,
                'customer': customer,
                'carts': carts,
                'qty': qty,
                'total': total,
                'discount': discount,
                'grand_total': grand_total,
                'form_data': form_data,
            }
            return render(request, 'checkout.html', details)

        for cart in carts:
            orderpr = OrderProduct(
                order_id = order.id,
                user_id = currentuser.id,
                product_id = cart.product_id,
                qty = cart.qty,
                price = cart.product.price,
                amount = cart.amount
            )
            orderpr.save()
        
        Cart.objects.filter(user_id=currentuser.id).delete()
        messages.success(request, "Order has been placed. Thank You 😊")
        return redirect('ShopHome')
    
    details = {
        'myuser':myuser,
        'customer':customer,
        'carts':carts,
        'qty':qty,
        'total':total,
        'discount':discount,
        'grand_total':grand_total,
    }
    
    return render(request, 'checkout.html', details)