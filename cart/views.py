from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from .utils import get_or_create_cart

def view_cart(request):
    cart = get_or_create_cart(request)
    context = {'cart': cart}
    return render(request, 'view-cart.html', context)

@csrf_protect
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    if quantity > product.inventory:
        messages.error(request, 'הכמות המבוקשת לא קיימת במלאי')
        return JsonResponse({'success': False})

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        if item.quantity + quantity > product.inventory:
            messages.error(request, 'הכמות המבוקשת לא קיימת במלאי')
            return JsonResponse({'success': False})
  
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    messages.success(request, "המוצר נוסף בהצלחה")
    return JsonResponse({'success': True})

@csrf_protect
def remove_item(request):
    item_id = request.POST.get('item_id')
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return JsonResponse({'success': True})

@csrf_protect
def update_quantity(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity'))

    item = get_object_or_404(CartItem, id=item_id)
    product = item.product

    if quantity > 0:
        if quantity > product.inventory:
            messages.error(request, 'הכמות המבוקשת לא קיימת במלאי')
            return JsonResponse({'success': False})
        item.quantity = quantity
        item.save()
        messages.success(request, 'Quantity updated.')
    else:
        item.delete()
        messages.success(request, 'Item removed from cart.')

    return JsonResponse({'success': True})