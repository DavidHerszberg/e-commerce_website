from django.db import models
from django.contrib.auth.models import User

DEFAULT_STATUS_ID = 1
DEFAULT_STATUS_NAME = "חדשה"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField(verbose_name="זמן", auto_now=True, auto_now_add=False)
    status = models.ForeignKey("orders.Status", default=DEFAULT_STATUS_ID, on_delete=models.SET_DEFAULT, verbose_name="סטטוס")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="סך הכל")
    vat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="מעמ")
    paid = models.BooleanField(verbose_name="שולם")
    #payment = models.OneToOneField('accounting.Payment')

    class Meta:
        verbose_name = "הזמנה"
        verbose_name_plural = "הזמנות"


class OrderItem(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_included = models.BooleanField(default=True)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product = models.ForeignKey('products.Product', null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name="שם")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "סטטוס"
        verbose_name_plural = "סטטוסים"

#initialize default status
try:
    Status.objects.get(id=DEFAULT_STATUS_ID)
except Status.DoesNotExist:
    default = Status(id=DEFAULT_STATUS_ID, name=DEFAULT_STATUS_NAME)
    default.save()