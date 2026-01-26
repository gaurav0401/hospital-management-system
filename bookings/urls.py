from django.urls import path
from .views import cancel_booking , admin_cancel_booking

urlpatterns = [
    path('cancel/<int:pk>/', cancel_booking, name='cancel_booking'),
    path('admin/cancel/<int:pk>/', admin_cancel_booking, name='admin_cancel_booking'),

]
