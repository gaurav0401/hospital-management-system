from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Availability
from django.contrib import messages
from django.shortcuts import get_object_or_404
from bookings.models import Booking


@login_required
def doctor_dashboard(request):
    doctor = request.user

    my_availabilities = Availability.objects.filter(
        doctor=doctor
    ).order_by('date', 'start_time')

    my_appointments = Booking.objects.filter(
        doctor=doctor
    ).select_related('patient', 'availability').order_by(
        'availability__date',
        'availability__start_time'
    )

    return render(
        request,
        'doctor_dashboard.html',
        {
            'doctor': doctor,
            'availabilities': my_availabilities,
            'appointments': my_appointments,
        }
    )


@login_required
@login_required
def add_availability(request):
    if request.method == "POST":
        Availability.objects.create(
            doctor=request.user,   
            date=request.POST.get('date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time')
        )
        return redirect('doctor_dashboard')

    return render(request, 'add_availability.html')


@login_required
def edit_availability(request, pk):
    slot = get_object_or_404(
        Availability,
        pk=pk,
        doctor=request.user
    )

    if slot.is_booked:
        messages.error(request, "Booked slots cannot be edited.")
        return redirect('doctor_dashboard')

    if request.method == "POST":
        slot.date = request.POST.get('date')
        slot.start_time = request.POST.get('start_time')
        slot.end_time = request.POST.get('end_time')
        slot.save()

        messages.success(request, "Availability updated.")
        return redirect('doctor_dashboard')

    return render(request, 'edit_availability.html', {'slot': slot})


@login_required
def delete_availability(request, pk):
    slot = get_object_or_404(
        Availability,
        pk=pk,
        doctor=request.user
    )

    if slot.is_booked:
        messages.error(request, "Booked slots cannot be deleted.")
        return redirect('doctor_dashboard')

    slot.delete()
    messages.success(request, "Availability deleted.")
    return redirect('doctor_dashboard')
