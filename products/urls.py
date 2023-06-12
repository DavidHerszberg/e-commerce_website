from django.urls import path
from . import views

urlpatterns = [
    path('<str:product_id>', views.product_page, name='product_page'),
]