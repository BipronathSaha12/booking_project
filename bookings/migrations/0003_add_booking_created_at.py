from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_remove_booking_created_at_remove_booking_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
