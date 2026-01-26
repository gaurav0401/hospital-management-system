"""
URL configuration for hms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from accounts.views import signup, dashboard, logout_view , home , login_view, admin_dashboard
from doctors.views import doctor_dashboard, add_availability
from bookings.views import patient_dashboard, book_slot

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls , name='admin'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('doctor/', include('doctors.urls')),
    path('bookings/', include('bookings.urls')),
    path('accounts/', include('accounts.urls')),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'), 
    path('dashboard/', dashboard , name='dashboard'),
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('doctor/add/', add_availability, name='add_availability'),
    path('patient/', patient_dashboard, name='patient_dashboard'),
    path('book/<int:slot_id>/', book_slot, name='book_slot'),
    path('logout/', logout_view, name='logout'),
]