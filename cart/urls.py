from django.urls import path
from . import views

urlpatterns = [
    path('view-cart', views.view_cart, name='view-cart'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('remove-item', views.remove_item, name='remove-item'),
    path('update-item', views.update_quantity, name='update-item'),
]
