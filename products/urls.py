from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<str:product_id>', views.product_page, name='product_page'),
]