from django.shortcuts import render, redirect
#just for the demo
from django.http import HttpResponse
from .models import  CustomUser, MainUser, Booking, Room
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.

def landing_page(request):
    return render(request, "core/index.html")

#login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
    
        user = authenticate(request, username=username, password=password)

        print(request.POST)

        if user is not None:
           login(request, user)
           return redirect('dashboard')
    
        else:
            return render(request, 'core/login.html', {'error': "Invalid Credential"}) 

    return render(request, 'core/login.html')

#sign up view
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
   #     role = request.POST.get("role", "user") #default to 'user'

        print(request.POST)

       # if MainUser.objects.filter(username=username).exists():
          #  return render(request, 'core/signup.html', {'error': "Username already exists"})

        #create customerUser
        new_user = CustomUser.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
     #   role=role
            )

       #create mainuser profile
        MainUser.objects.create(
            user=new_user,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number
        )

        return redirect("login")  # Redirect to login page after successful signup
    return render(request, 'core/signup.html')

#logout view
def logout_view(request):
    logout(request, CustomUser)
    return redirect('landing_page')

@login_required
def  Booking_view(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room = Room.objects.get(room_number=room_number)
        user = request.user
        Booking.objects.create(
            user=user,
            room=room,
            date_booked=datetime.datetime.now(),
            status='pending'
        )
        return redirect('dashboard')  # Redirect to dashboard after booking
    
    if user.is_authenticated:
        rooms = Room.objects.all()
        return render(request, 'core/booking.html', {'rooms': rooms})
    
    if room.gender != request.user.gender:
        reject_message = "Sorry, you cannot book this room as it is not suitable for your gender."
        return render(request, 'core/booking.html', {'reject_message': reject_message})

    return render(request, 'core/booking.html')   


@login_required
def dashboard_view(request):
   """  user = request.user
    bookings = Booking.objects.filter(user=user)
    all_bookings = Booking.objects.all()
    
    return render(request, 'core/dashboard.html', {'bookings': bookings, 'all_bookings': all_bookings})
 """
   return HttpResponse("Welcome to the dashboard")

@login_required
def cancel_booking_view(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        booking.delete()
    return redirect('dashboard')

@login_required
def room_view(request):
    rooms = Room.objects.all()
    return render(request, 'core/rooms.html', {'rooms': rooms})
