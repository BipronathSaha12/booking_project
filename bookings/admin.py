from django.contrib import admin
from .models import Service, Booking


class BookingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.qr_code:
            from .utils import generate_qr
            generate_qr(obj)


admin.site.register(Booking, BookingAdmin)
admin.site.register(Service)