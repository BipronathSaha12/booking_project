from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Service, Booking
from .forms import BookingForm
from .utils import generate_qr
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe

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
    return render(request, "bookings/success.html", {"booking": booking})


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
