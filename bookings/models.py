from django.db import models
from django.contrib.auth.models import User
from .utils import generate_qr
from django.utils import timezone

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    paid = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:
            generate_qr(self)

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"
