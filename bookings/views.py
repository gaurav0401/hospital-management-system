from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from doctors.models import Availability
from django.contrib import messages
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from utils.email_service import send_email
from .models import Booking


@login_required
def patient_dashboard(request):
    patient = request.user

    # Patient's booked appointments
    my_appointments = Booking.objects.filter(
        patient=patient
    ).select_related('doctor', 'availability').order_by(
        'availability__date',
        'availability__start_time'
    )

    # Available slots (not booked)
    available_slots = Availability.objects.filter(
        is_booked=False
    ).order_by('date', 'start_time')

    return render(
        request,
        'patient_dashboard.html',
        {
            'patient': patient,
            'my_appointments': my_appointments,
            'available_slots': available_slots,
        }
    )
from django.db import transaction
from django.shortcuts import redirect
from .models import Booking
from doctors.models import Availability

# @transaction.atomic
# def book_slot(request, slot_id):
#     slot = Availability.objects.select_for_update().get(id=slot_id)

#     if slot.is_booked:
#         raise Exception("Already booked")

#     slot.is_booked = True
#     slot.save()

#     Booking.objects.create(
#         doctor=slot.doctor,
#         patient=request.user,
#         availability=slot
#     )

#     return redirect('patient_dashboard')

@transaction.atomic
def cancel_booking(request, pk):
    booking = get_object_or_404(
        Booking,
        pk=pk,
        patient=request.user
    )

    slot = booking.availability
    slot.is_booked = False
    slot.save()

    booking.delete()

    messages.success(request, "Appointment cancelled successfully.")
    return redirect('patient_dashboard')


from accounts.decorators import admin_required

@login_required
@admin_required
def admin_cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    slot = booking.availability
    slot.is_booked = False
    slot.save()

    booking.delete()

    messages.success(request, "Appointment cancelled by admin.")
    return redirect('admin_dashboard')



from utils.google_calendar import create_calendar_event
from datetime import datetime


@transaction.atomic
def book_slot(request, slot_id):
    slot = get_object_or_404(
        Availability,
        id=slot_id,
        is_booked=False
    )

    # 1️ Create booking (DB-critical)
    booking = Booking.objects.create(
        patient=request.user,
        doctor=slot.doctor,
        availability=slot
    )

    slot.is_booked = True
    slot.save()

    # 2️ Prepare datetime
    start_dt = datetime.combine(slot.date, slot.start_time)
    end_dt = datetime.combine(slot.date, slot.end_time)

    # 3️ Google Calendar (NON-critical, safe)
    doctor_event = None
    patient_event = None

    try:
        doctor_event = create_calendar_event(
            user=slot.doctor,
            title=f"Appointment with {request.user.first_name}",
            description="Patient appointment has been booked successfully.",
            start_dt=start_dt,
            end_dt=end_dt
        )

        patient_event = create_calendar_event(
            user=request.user,
            title=f"Appointment with Dr. {slot.doctor.first_name}",
            description="Doctor appointment has been booked successfully.",
            start_dt=start_dt,
            end_dt=end_dt
        )

    except Exception:
        #  NEVER crash booking for calendar issues
        pass

    # 4️ Save event IDs (if created)
    if doctor_event:
        booking.doctor_calendar_event_id = doctor_event.get("id")

    if patient_event:
        booking.patient_calendar_event_id = patient_event.get("id")

    booking.save()

    send_email(
    action="BOOKING_CONFIRMATION",
    to_email=request.user.email,
    data={
        "name": request.user.first_name,
        "doctor": f"Dr. {slot.doctor.first_name}",
        "date": slot.date.strftime("%d-%m-%Y"),
        "time": f"{slot.start_time} - {slot.end_time}",
    }
    )

    # 5️ User feedback
    if request.user.google_token:
        messages.success(
            request,
            "Appointment booked and synced with Google Calendar."
        )
    else:
        messages.success(
            request,
            "Appointment booked successfully. Connect Google Calendar to sync events."
        )

    return redirect('patient_dashboard')

