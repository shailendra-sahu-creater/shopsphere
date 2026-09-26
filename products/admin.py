from django.contrib import admin
from .models import Product, Order,  OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    ("Pending", "Pending"),
    ("Confirmed", "Confirmed"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ["name", "phone",  "total", "status", "created_at"]
    list_editable = ["status"]
    ordering = ["-created_at"]
    search_fields = ["name", "phone"]
    list_filter = ["created_at"]
    

admin.site.register(Order,OrderAdmin)


class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "price","stock", "created_at"]
    ordering = ["-created_at"]
    list_filter = ["price"]
    
admin.site.register(Product, ProductAdmin)
