from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Availability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} | {self.date} {self.start_time}-{self.end_time}"
