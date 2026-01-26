from django.urls import path
from .views import (
    doctor_dashboard,
    add_availability,
    edit_availability,
    delete_availability,
)

urlpatterns = [
    path('', doctor_dashboard, name='doctor_dashboard'),
    path('add/', add_availability, name='add_availability'),
    path('edit/<int:pk>/', edit_availability, name='edit_availability'),
    path('delete/<int:pk>/', delete_availability, name='delete_availability'),
]
