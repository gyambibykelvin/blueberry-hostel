# BlueBerry Hostel Management System

BlueBerry Hostel is a web-based hostel booking system built with Django. It allows users to browse available rooms, make bookings, and manage their reservations through a structured dashboard interface.

## Live Application
https://blueberry-hostel.onrender.com/

## Overview
This system is designed to simplify hostel accommodation management for students. It provides a centralized platform for handling room allocation, booking status tracking, and user profile management.

## Features
### Authentication
* User registration and login
* Secure authentication using Django’s authentication system
* Password reset via email

### Room Management
* Display available rooms
* Room capacity tracking
* Gender-based room assignment

### Booking System
* Create bookings for available rooms
* Prevent duplicate bookings
* Booking status workflow:
  * Pending
  * Approved
  * Rejected

### User Dashboard
* Overview metrics (total rooms, bookings, status counts)
* Recent booking activity
* Booking management (including cancellation)

### Profile Management
* Update user information
* Upload and manage profile picture(Cloudinary)

## Technology Stack
* Backend: Django
* Frontend: HTML, CSS, JavaScript
* Database:
  * SQLite (demo purposes)
* Deployment: Render
* Static Files: WhiteNoise

## Installation

```bash
git clone https://github.com/gyambibykelvin/blueberry-hostel.git
cd blueberry-hostel

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## Environment Variables

Configure the following environment variables:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

## Project Structure

```
backend/
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── static/
│
├── backend/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
```

## Known Limitations

* Media files (profile images) are not persistently stored in production
* Render free tier introduces cold-start delays
* No real-time notification system


## Future Improvements
* Real-time notifications
* Payment system integration
* Improved admin workflow for booking approvals
* Performance optimization and caching
* Database improvement(PostgreSQL)

## Author
Kelvin Anane Gyambiby
Software Engineering Student

## License
This project is intended for educational purposes.
