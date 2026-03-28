from django.shortcuts import render, redirect
#just for the demo
from django.http import HttpResponse
from .models import  CustomUser, MainUser, Booking, Room
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.

now = datetime.datetime.now()

def landing_page(request):
    return render(request, "core/index.html", {'datetime': now.year})

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
    logout(request)
    return redirect('landing_page')

#booking view
@login_required
def booking_view(request):
    user = request.user

    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room = Room.objects.get(room_number=room_number)

        # VALIDATION: gender check BEFORE booking
        if room.gender != user.profile.gender:
            return render(request, 'core/dashboard.html', {
                'error': "Room not suitable for your gender"
            })

        Booking.objects.create(
            user=user,
            room=room,
            date_booked=datetime.datetime.now(),
            status='pending'
        )

        return redirect('dashboard')

    return redirect('dashboard')


@login_required
def dashboard_view(request):
    user = request.user

    #All user bookings
    bookings = Booking.objects.filter(user=user).order_by('-date_booked')

    #Recent booking (latest)
    recent_booking = bookings.first()

    #Filter rooms by gender (CRITICAL UX FIX) #will be right back
    user_gender = request.user.profile.gender
    rooms = Room.objects.filter(gender=user_gender)


    """  user_gender = user.profile.gender
    rooms = Room.objects.filter(gender=user_gender) """

    #Stats
    total_bookings = bookings.count()
    pending = bookings.filter(status='pending').count()
    approved = bookings.filter(status='approved').count()
    rejected = bookings.filter(status='rejected').count()
    available_rooms = rooms.count()

    context = {
        'bookings': bookings,
        'recent_booking': recent_booking,
        'rooms': rooms,
        'total_bookings': total_bookings,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'available_rooms': available_rooms,
        'datetime': now.year
    }

    return render(request, 'core/dashboard.html', context)


#cancel booking logic
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
