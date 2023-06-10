from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpRequest
from .models import Product



# Create your views here.
def serve_product_image(request: HttpRequest, image_name: str) -> HttpResponse:
    image_path = f'product_images/{image_name}'

    try:
        with default_storage.open(image_path, 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/jpeg')
            return response
    except IOError:
        # Return a 404 response if the image file is not found
        return HttpResponse(status=404)
    
def serve_attribute_image(request: HttpRequest, image_name: str) -> HttpResponse:
    image_path = f'attribute_images/{image_name}'

    try:
        with default_storage.open(image_path, 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/jpeg')
            return response
    except IOError:
        # Return a 404 response if the image file is not found
        return HttpResponse(status=404)
    
def product_page(request: HttpRequest, product_id: str) -> HttpResponse:
    try:
        product = Product.objects.get(store_id=product_id)
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    page = f"""<h1> {product.hebrew_name} </h1>\n
        <h2> {product.english_name}</h2>\n
        <h3> {product.description}</h3>\n
        <img src="/{product.main_image.image}" />"""
    return HttpResponse(page)
