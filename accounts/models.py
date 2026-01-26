from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Common fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # Doctor-only
    specialty = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)

    # Patient-only
    date_of_birth = models.DateField(blank=True, null=True)
    google_token = models.JSONField(null=True, blank=True)

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return (
                today.year
                - self.date_of_birth.year
                - ((today.month, today.day) <
                   (self.date_of_birth.month, self.date_of_birth.day))
            )
        return None
