from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','full_name',"payment_method"]
    list_filter = ['order_status','payment_status']
    inlines = [OrderItemInline]