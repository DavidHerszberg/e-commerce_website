"""legima URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .shared import admin_site_titles
from . import views
from products import views as product_views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('site-images/<str:image_name>', views.serve_site_image, name='serve_site_image'),
    path('product_images/<str:image_name>', product_views.serve_product_image, name='serve_product_image'),
    path('attribute_images/<str:image_name>', product_views.serve_attribute_image, name='serve_attribute_image'),
    path('products/', include('products.urls')),
    path('tinymce/',include('tinymce.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('orders.urls'))
]


admin.site.site_header = admin_site_titles['site_header']           
admin.site.index_title = admin_site_titles['index_title']              
admin.site.site_title = admin_site_titles['site_title']