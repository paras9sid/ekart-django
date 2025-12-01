import datetime, json, razorpay
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

# sending email
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from store.models import Product


from ekart.settings import RZP_KEY_ID,RZP_KEY_SECRET
client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

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

    # move the cart items to product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id 
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.qty = item.qty
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # above =- variation field is not set , because to assign manytomanyfield we have to save the order first - cant assign directly
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id) #save ahs generted the order product id for us
        orderproduct.variations.set(product_variation)
        orderproduct.save()
    
    
        #reduce the quantity of sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.qty
        product.save()



    # Clear the cart <- outside for loop
    CartItem.objects.filter(user=request.user).delete()

    # send order email to customers 
    mail_subject = "Than you for your order"
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })

    try:
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        messages.success(request, 'Check your email.')
    except Exception as e:
        print("Email sending failed:", e)
        messages.error(request, 'Order complete, but email sending failed.')

    # send order number and transaction id back to sendData via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)
    # return render(request, 'orders/payments.html')


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
            data.pin_code = form.cleaned_data['pin_code']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.payment_method = request.POST['payment_method']
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

            # Razorpay Payment
            DATA = {
                "amount": float(data.order_total) * 100,
                "currency": "INR",
                "receipt": "receipt #"+data.order_number,
                # "notes": {
                #     "key1": "value3",
                #     "key2": "value2"
                # } 
            }
            rzp_order = client.order.create(data=DATA) 
            rzp_order_id = rzp_order['id']
            print(rzp_order)    

            #order payment page
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'rzp_order_id': rzp_order_id,
                'RZP_KEY_ID': RZP_KEY_ID,
                'rzp_amount': float(data.order_total) * 100,
            
            }
            return render(request, 'orders/payments.html', context)
    # else:
    #     print("in else block error")
    #     return redirect('checkout')
    #     # return render(request, 'orders/payments.html')
        else:
            print(form.errors)

    # add message email add id error or validate with js code in templates
    return redirect('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        #subtotal field in frontned invoice
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.qty

        #for getting payment/transaID in context tor eflect on front end
        payment = Payment.objects.get(payment_id=transID)

        context={
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID' : payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')