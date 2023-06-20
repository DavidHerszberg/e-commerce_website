from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from products.models import Product
import json

VAT_RATE = 17
# Create your views here.

@csrf_exempt
@require_POST
def create_order(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    order = Order(total_price = 0, vat = 0, paid = False)
    order.save()

    request_data = json.loads(request.body)
    for item in request_data.get('items'):
        item_obj = OrderItem(
            name = item['name'],
            quantity = item['quantity'],
            price = float(item['price']),
            order = order
        )
        if hasattr(item, 'product_id'):
            try:
                item_obj.product = Product.objects.get(item['product_id'])
            except Product.DoesNotExist:
                pass
        item_obj.vat = item_obj.price / 100 * VAT_RATE
        item_obj.save()

        order.total_price += item_obj.price * item_obj.quantity
        order.vat += item_obj.vat * item_obj.quantity
        order.save()

    if user:
        order.user = user
    
    order.save()

    return HttpResponse("order created", status=201)

    