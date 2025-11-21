import datetime, json
from django.http import HttpResponse
from django.shortcuts import render, redirect

from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment


# Create your views here.
def payments(request):
    body = json.loads(request.body)
    # print(body)
    order=Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    #store transactions details payment model
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save() 
    return render(request, 'orders/payments.html')


def place_order(request,total=0, qty=0):
    
    current_user = request.user

    # if the cart count is <= 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total = total + (cart_item.product.price * cart_item.qty)
        qty += cart_item.qty
    tax = (5 * total)/100 # tax is 5%
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing info inside Order Table
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

            #generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d") #2025(Y)11(mt)18(dt) <- format like this date time

            order_number = current_date + str(data.id) # <- convert id int into str format for concatenation w/o error
            data.order_number = order_number            
            data.save()

            #order payment page
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        print("in else block error")
        return redirect('checkout')
        # return render(request, 'orders/payments.html')