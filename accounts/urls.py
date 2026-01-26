from django.urls import path
from .views import admin_dashboard, doctor_signup, google_callback, google_login, patient_signup , google_disconnect

urlpatterns = [
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('signup/doctor/', doctor_signup, name='doctor_signup'),
    path('signup/patient/', patient_signup, name='patient_signup'),
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'), 
    path('google/disconnect/', google_disconnect, name='google_disconnect'),
 
]
