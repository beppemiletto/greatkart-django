import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import datetime
import json


def payments(request):
    current_user = request.user
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user=current_user, is_ordered=False, order_number= body['orderID'])
    payment = Payment(
        user=current_user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
        payer_id=body['payer']['payer_id'],
        payer_mail=body['payer']['email_address'],
        payer_surname=body['payer']['name']['surname'],
        payer_given_name=body['payer']['name']['given_name'],
        )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to the Order Product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = current_user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()







    # Reduce the quantity of sold products

    # Clear the cart

    # Send order received email to customer

    # Send order number and transaction id back to sendData method via JsonResponse

    return render(request, 'orders/payments.html')

def place_order(request, total=0, quantity=0,):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    # return HttpResponse("<H2>Current user: {} </H2><br><H2>Cart items number : {} </H2>".format(current_user,cart_count))
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    # return HttpResponse("<H2>Taxes: {} € </H2><br><H2>Grand total: {} €</H2>".format(tax,grand_total))
    if request.method == 'POST':
        form = OrderForm(request.POST)
        # return HttpResponse("<H1>Entered th POST clause</H1><br>Got the form that is {}".format(form.is_valid()))
        if form.is_valid():
            # Store all the billing information inside Order Table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'grand_total': grand_total,
                'tax': tax,
            }

            # return HttpResponse('Ok the form is valid and I saved the Order Record')
            return render(request, 'orders/payments.html', context)
        else:
            return HttpResponse("<H1>Entered th POST clause</H1><br>Got the following form that is NOT VALID <br> {}".format(form))

    else:
        return redirect('checkout')



