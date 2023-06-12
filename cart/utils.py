from .models import Cart


def get_or_create_cart(request):
    if request.user.is_authenticated:
        # Retrieve or create the cart associated with the authenticated user
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        # Retrieve the session-based cart or create a new one
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = None
        else:
            cart = None

        if not cart:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id

    return cart