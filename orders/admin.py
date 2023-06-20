from django.contrib import admin
from django.http.request import HttpRequest
from .models import Order, Status, DEFAULT_STATUS_ID

class OrderAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
class StatusAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        if obj and obj.id == DEFAULT_STATUS_ID:
            return False
        return super().has_delete_permission(request, obj)

# Register your models here.

admin.site.register(Order, OrderAdmin)
admin.site.register(Status, StatusAdmin)