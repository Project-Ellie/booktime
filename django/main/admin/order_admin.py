from django.contrib import admin
from main import models


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "address1",
        "address2",
        "city",
        "country",
    )
    readonly_fields = ("user",)


class BasketLineInline(admin.TabularInline):
    model = models.BasketLine
    raw_id_fields = ("product",)


class BasketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "count")
    list_editable = ("status",)
    list_filter = ("status",)
    inlines = (BasketLineInline,)


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    raw_id_fields = ("product",)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status")
    list_editable = ("status",)
    list_filter = ("status", "shipping_country", "date_added")
    inlines = (OrderLineInline,)
    fieldsets = (
        (None, {"fields": ("user", "status")}),
        (
            "Billing info",
            {
                "fields": (
                    "billing_name",
                    "billing_address1",
                    "billing_address2",
                    "billing_zip_code",
                    "billing_city",
                    "billing_country",
                )
            },
        ),
        (
            "Shipping info",
            {
                "fields": (
                    "shipping_name",
                    "shipping_address1",
                    "shipping_address2",
                    "shipping_zip_code",
                    "shipping_city",
                    "shipping_country",
                )
            },
        ),
    )


class CentralOfficeOrderLineInline(admin.TabularInline):
    model = models.OrderLine
    readonly_fields = ("product",)


class CentralOfficeOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status")
    list_editable = ("status",)
    readonly_fields = ("user",)
    list_filter = ("status", "shipping_country", "date_added")
    inlines = (CentralOfficeOrderLineInline,)
    fieldsets = (
        (None, {"fields": ("user", "status")}),
        (
            "Billing info",
            {
                "fields": (
                    "billing_name",
                    "billing_address1",
                    "billing_address2",
                    "billing_zip_code",
                    "billing_city",
                    "billing_country",
                )
            },
        ),
        (
            "Shipping info",
            {
                "fields": (
                    "shipping_name",
                    "shipping_address1",
                    "shipping_address2",
                    "shipping_zip_code",
                    "shipping_city",
                    "shipping_country",
                )
            },
        ),
    )


class DispatchersOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "shipping_name",
        "date_added",
        "status",
    )
    list_filter = ("status", "shipping_country", "date_added")
    inlines = (CentralOfficeOrderLineInline,)
    fieldsets = (
        (
            "Shipping info",
            {
                "fields": (
                    "shipping_name",
                    "shipping_address1",
                    "shipping_address2",
                    "shipping_zip_code",
                    "shipping_city",
                    "shipping_country",
                )
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=models.Order.PAID)


admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Basket, BasketAdmin)
admin.site.register(models.Order, OrderAdmin)
