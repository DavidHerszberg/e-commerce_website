from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpRequest

def home(request):
    return render(request, 'home-own.html')

def serve_site_image(request, image_name):
    image_path = f'site-images/{image_name}'

    try:
        with default_storage.open(image_path, 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/jpeg')
            return response
    except IOError:
        # Return a 404 response if the image file is not found
        return HttpResponse(status=404)