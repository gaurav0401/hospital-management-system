from django.conf import settings
from django.db import models
from doctors.models import Availability

User = settings.AUTH_USER_MODEL

class Booking(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_bookings")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_bookings")
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


