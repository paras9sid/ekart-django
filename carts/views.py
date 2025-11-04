from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist

from store.models import Product
from .models import Cart, CartItem

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create
    return cart

def add_cart(request, product_id):

    if request.method == 'POST':
        # taking value from browser url # both bwlo coming from product_detail.html
        color = request.POST['color']
        size = request.POST['size']
        print(color, size)


    # Before POST mehtod - for get method to check # taking value from browser url # both bwlo coming from product_detail.html
    # color = request.GET['color']
    # size = request.GET['size']
    # print(color, size)
    # return HttpResponse(color + ' ' +size)
    # exit()

    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request)) # get the cart using the cart id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.qty += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            qty = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.qty > 1:
        cart_item.qty -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')
    

def cart(request, total=0, qty=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total = total + (cart_item.product.price * cart_item.qty)
            qty = qty + cart_item.qty
        tax = (5 * total)/100 # tax is 5%
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'qty': qty,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total' : grand_total
    }
    return render(request, 'store/cart.html', context)