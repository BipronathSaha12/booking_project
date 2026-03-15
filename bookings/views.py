import logging
import os
from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from xhtml2pdf import pisa

from .forms import BookingForm
from .models import Service, Booking
from .utils import generate_qr

import stripe

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    services = Service.objects.all()
    return render(request, "bookings/home.html", {"services": services})

@login_required
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.date = form.cleaned_data['date']  # date assign করতে হবে
            booking.save()  # QR code auto generate in model save()

            # Stripe Checkout Session
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': service.name,
                            },
                            'unit_amount': int(service.price * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(
                        f"/stripe-success/{booking.id}/"
                    ),
                    cancel_url=request.build_absolute_uri("/"),
                )
                return redirect(session.url)
            except stripe.error.StripeError:
                messages.error(
                    request,
                    "Payment service is temporarily unavailable. Your booking has been saved, please try again.",
                )
                return redirect('dashboard')
            except Exception:
                messages.error(request, "An unexpected error occurred. Please try again.")
                return redirect('dashboard')
    else:
        form = BookingForm()

    return render(request, "bookings/service_detail.html", {
        "service": service,
        "form": form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY
    })


@login_required
def stripe_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.paid = True
    booking.save()
    if not booking.qr_code:
        generate_qr(booking)

    # Send ticket PDF to user's email
    pdf_bytes = render_ticket_pdf(booking)
    if pdf_bytes:
        emailed = send_ticket_email(booking, pdf_bytes)
        if emailed and booking.user.email:
            messages.success(request, f"Ticket emailed to {booking.user.email}.")

    return render(request, "bookings/success.html", {"booking": booking})


def render_ticket_pdf(booking):
    """Render the ticket template to a PDF in memory and return bytes."""
    template = get_template("bookings/pdf_ticket.html")
    html = template.render({"booking": booking})

    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer, link_callback=link_callback)
    if pisa_status.err:
        return None
    buffer.seek(0)
    return buffer.read()


def send_ticket_email(booking, pdf_bytes):
    """Send ticket PDF to the booking user's email address."""
    user = booking.user
    recipient = user.email or None
    if not recipient:
        return

    subject = f"Your booking ticket for {booking.service.name}"
    body = (
        f"Hi {user.get_full_name() or user.username},\n\n"
        "Thank you for your booking. Your ticket is attached as a PDF.\n\n"
        "See you soon!"
    )

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient],
    )
    email.attach(f"ticket_{booking.id}.pdf", pdf_bytes, "application/pdf")
    try:
        email.send(fail_silently=False)
        return True
    except Exception as exc:
        # Don't block the user flow if email cannot be sent.
        logger.exception("Failed to send ticket email")
        return False


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access static and media files.
    """
    if uri.startswith(settings.STATIC_URL):
        path = uri.replace(settings.STATIC_URL, "")
        result = finders.find(path)
        if result:
            return result
    if uri.startswith(settings.MEDIA_URL):
        path = uri.replace(settings.MEDIA_URL, "")
        return os.path.join(settings.MEDIA_ROOT, path)
    return uri


@login_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if not booking.paid:
        messages.error(request, "Please complete payment before downloading the ticket.")
        return redirect('dashboard')

    template = get_template("bookings/pdf_ticket.html")
    html = template.render({"booking": booking, "request": request})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="ticket_{booking.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        messages.error(request, "Unable to generate PDF ticket at this time.")
        return redirect('dashboard')
    return response


@login_required
def pay_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.paid:
        messages.info(request, "This booking is already paid.")
        return redirect('dashboard')

    service = booking.service
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': service.name,
                    },
                    'unit_amount': int(service.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                f"/stripe-success/{booking.id}/"
            ),
            cancel_url=request.build_absolute_uri("/"),
        )
        return redirect(session.url)
    except stripe.error.StripeError:
        messages.error(
            request,
            "Payment service is temporarily unavailable. Please try again later.",
        )
        return redirect('dashboard')
    except Exception:
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect('dashboard')


@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "bookings/dashboard.html", {"bookings": bookings})
