from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.
class OrderProductInLine(admin.TabularInline):
    model = OrderProduct
    extra = 0 # will remove default 3 extra lines for details provided by inbuilt django
    # editable fields converted tor ead only so none can change customer order requirements data in admin section
    readonly_fields = ['payment', 'user', 'product', 'qty', 'product_price', 'ordered', 'variations']
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'pin_code', 'order_total', 'tax', 'status', 'payment_method', 'ip', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInLine]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
