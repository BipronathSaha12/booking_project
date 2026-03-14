import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr(booking):
    data = f"Booking ID: {booking.id}\nService: {booking.service.name}\nUser: {booking.user.username}"
    qr_img = qrcode.make(data)
    buffer = BytesIO()
    qr_img.save(buffer)
    buffer.seek(0)
    booking.qr_code.save(f"booking_{booking.id}.png", File(buffer), save=False)
    booking.save()