from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
