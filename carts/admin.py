from django.contrib import admin
from .models import Order, OrderItem, PromotionCode

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(PromotionCode)
class PromotionCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_amount",
        "is_used",
        "created_at",
    )
    list_filter = ("is_used",)
    search_fields = ("code",)