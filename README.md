# 🏥 DocEase – Mini Hospital Management System (HMS)

DocEase is a role-based Mini Hospital Management System built using **Django**, designed to manage **doctor availability**, **patient appointment booking** and  **Google Calendar synchronization**.

This project demonstrates real-world backend concepts such as:
- Role-based authentication
- Transaction-safe booking
- External API integration (Google Calendar)
- Serverless Email Service (offline AWS Lambda based)
- Clean separation of concerns

---

## 🚀 Features

### 👤 User Roles
- **Admin**
- **Doctor**
- **Patient**

---

### 🔐 Authentication & Authorization
- Secure login & signup
- Password hashing (Django default)
- Role-based access control
- Admin-only dashboard access

---

### 👨‍⚕️ Doctor Features
- Manage personal profile (name, speciality, experience, etc.)
- Create availability slots (date & time)
- View own availability only
- View booked appointments
- Cancel appointments
- Google Calendar integration

---

### 🧑‍🦱 Patient Features
- View doctors with speciality & experience
- View available slots
- Book appointments (race-condition safe)
- View upcoming appointments
- Cancel appointments
- Google Calendar integration
- Patient info card in dashboard

---

### 🛠 Admin Features
- View all doctors & patients
- View system-wide appointments
- Cancel any appointment
- Monitor platform usage

---

### 📅 Google Calendar Integration
- OAuth2 based authentication
- One-time calendar connection per user
- Events created on booking:
  - Doctor’s calendar
  - Patient’s calendar
- Events removed on cancellation
- Handles same Google account edge cases
- Graceful fallback if calendar not connected

---



## 🧱 Tech Stack

### Backend
- **Python**
- **Django**
- **Django ORM**
- **SQLite**
- **AWS Lambda**

### Frontend
- **HTML**
- **Bootstrap 5**
- **Django Templates**

### Integrations
- **Google Calendar API**
- **OAuth2**
- **Serverless Service**


---

## 📁 Project Structure

### Architecture
<img width="593" height="788" alt="image" src="https://github.com/user-attachments/assets/a71b8506-2931-4e39-b409-97c44de49589" />




### App Overview

- **accounts/** – User authentication, roles, and permissions  
- **doctors/** – Doctor profiles, availability, and details  
- **bookings/** – Appointment scheduling and management  
- **utils/**  
  - `google_calendar.py` – Google Calendar API integration
  - `email_service.py` - Serverless Email Service
- **templates/** – HTML templates for the application UI  
