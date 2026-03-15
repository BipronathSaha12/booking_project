# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),  # My Bookings
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('stripe-success/<int:booking_id>/', views.stripe_success, name='stripe_success'),
    path('stripe-pay/<int:booking_id>/', views.pay_booking, name='pay_booking'),
    path('download-ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),
]
