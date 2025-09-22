from django.contrib import admin
from .models import Order, OrderLineItem, Coupon


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    extra = 0
    readonly_fields = ("line_total",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "email", "status", "total", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "email")
    readonly_fields = (
        "order_number",
        "subtotal",
        "discount_amount",
        "tax_amount",
        "total",
        "created_at",
        "updated_at",
    )
    inlines = [OrderLineItemInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "type", "value", "active", "uses", "starts_at", "ends_at")
    list_filter = ("active", "type")
    search_fields = ("code",)
