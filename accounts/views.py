from django.shortcuts import render, redirect
from django.contrib.auth import login , authenticate
from .models import User
from django.contrib import messages





def home(request):
    # If already logged in, send to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if role not in ['doctor', 'patient']:
            messages.error(request, "Please select a valid role.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists. Please choose another.")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role
        )

        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('dashboard')

    return render(request, 'signup.html')

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

def login_view(request):
    expected_role = request.GET.get('role')  # admin / doctor / patient / None

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, "Invalid username or password or User does not exist.")
            return redirect(request.path)

        # ADMIN-ONLY LOGIN CHECK
        if expected_role == 'admin':
            if not (user.is_superuser or user.role == 'admin'):
                messages.error(
                    request,
                    "You are not authorized to access the admin panel."
                )
                return redirect(request.path)

        #  DOCTOR / PATIENT ROLE CHECK
        elif expected_role:
            if user.role != expected_role:
                messages.error(
                    request,
                    f"You are not registered as a {expected_role}."
                )
                return redirect(request.path)

        # Passed all checks
        login(request, user)
        return redirect('admin_dashboard' if expected_role == 'admin' else 'dashboard')

    return render(request, 'login.html', {'expected_role': expected_role})

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def dashboard(request):
    user = request.user

    if user.is_superuser or user.role == 'admin':
        return redirect('admin_dashboard')

    if user.role == 'doctor':
        return redirect('doctor_dashboard')

    if user.role == 'patient':
        return redirect('patient_dashboard')

    # fallback
    return redirect('login')





from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')




from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from doctors.models import Availability
from bookings.models import Booking
from accounts.models import User

@login_required
@admin_required
def admin_dashboard(request):
    context = {
        'doctors': User.objects.filter(role='doctor'),
        'patients': User.objects.filter(role='patient'),
        'bookings': Booking.objects.select_related('doctor', 'patient'),
        'total_doctors': User.objects.filter(role='doctor').count(),
        'total_patients': User.objects.filter(role='patient').count(),
        'total_bookings': Booking.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DoctorSignupForm, PatientSignupForm

def doctor_signup(request):
    form = DoctorSignupForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = 'doctor'
        user.set_password(form.cleaned_data['password1'])
        user.save()
        messages.success(request, "Doctor account created successfully.")
        return redirect('login')

    return render(request, 'signup_doctor.html', {'form': form})


def patient_signup(request):
    form = PatientSignupForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = 'patient'
        user.set_password(form.cleaned_data['password1'])
        user.save()
        messages.success(request, "Patient account created successfully.")
        return redirect('login')

    return render(request, 'signup_patient.html', {'form': form})




from google_auth_oauthlib.flow import Flow
from django.conf import settings
from django.shortcuts import redirect
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def google_login(request):
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'client_secret.json'),
        scopes=SCOPES,
        redirect_uri='http://127.0.0.1:8000/accounts/google/callback/'
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    request.session['google_state'] = state
    return redirect(authorization_url)


from google.oauth2.credentials import Credentials

def google_callback(request):
    state = request.session['google_state']

    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        state=state,
        redirect_uri='http://127.0.0.1:8000/accounts/google/callback/'
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials

    request.user.google_token = {
    "token": credentials.token,
    "refresh_token": credentials.refresh_token,  
    "token_uri": credentials.token_uri,
    "client_id": credentials.client_id,
    "client_secret": credentials.client_secret,
    "scopes": credentials.scopes,}
    request.user.save()

    return redirect('dashboard')



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
import requests

@login_required
def google_disconnect(request):
    user = request.user

    if user.google_token:
        token = user.google_token.get('token')

        # Revoke token from Google
        requests.post(
            'https://oauth2.googleapis.com/revoke',
            params={'token': token},
            headers={'content-type': 'application/x-www-form-urlencoded'}
        )

        #  Remove token from DB
        user.google_token = None
        user.google_email = None
        user.save()

        messages.success(
            request,
            "Google Calendar disconnected successfully."
        )
    else:
        messages.info(
            request,
            "Google Calendar is not connected."
        )

    return redirect('dashboard')





