from django.shortcuts import render, redirect
from django.db.models import Count
from .models import  CustomUser, MainUser, Booking, Room
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages

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

        if user is not None:
           login(request, user)
           messages.success(request, "You have successfully login!")
           return redirect('dashboard')
    
        else:
            messages.error(request, 'Invalid Credential')
            return redirect('login') 

    return render(request, 'core/login.html')

#sign up view
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
   #     role = request.POST.get("role", "user") #default to 'user'

        #username taken
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username exists")
            return redirect('signup')
        
        #Email taken
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email Taken")
            return redirect('signup')

        #create customerUser
        new_user = CustomUser.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
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

        messages.success(request, "Account has been successfully created! Login to continue")
        return redirect('login')  # Redirect to login page after successful signup

    return render(request, 'core/signup.html')

#logout view
def logout_view(request):
    logout(request)
    messages.info(request,"You have been logout! Please login to continue")
    return redirect('landing_page')

#booking view
@login_required
def booking_view(request):
    user = request.user

    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room = Room.objects.get(room_number=room_number)

        #Prevent duplicate booking
        if Booking.objects.filter(user=user, room=room, status='pending').exists():
            messages.error(request, "You already booked this room and it is on pending")
            return redirect('dashboard')
        
        #capacity check
        #count current active bookings
        current_count = Booking.objects.filter(
            room=room,
            status__in = ['pending', 'approved']
        ).count()

        if current_count >= room.capacity:
            messages.error(request, "Room is almost full")
            return redirect('dashboard')

        #Gender validation
        if room.gender != user.profile.gender:
            messages.error(request, "Room not suitable for your gender.")
            return redirect('dashboard')
        
        #Restrict user to one active booking
        if Booking.objects.filter(
           user=user,
           status__in=['pending', 'approved']
        ).exists():
          messages.error(request, "You already have an active booking.")
          return redirect('dashboard')

        #Create booking
        Booking.objects.create(
            user=user,
            room=room,
            status='pending'
        )

        messages.success(request, "Booking submitted successfully.")
        return redirect('dashboard')

    return redirect('dashboard')


@login_required
def dashboard_view(request):
    user = request.user

    #All user bookings
    bookings = Booking.objects.filter(user=user).order_by('-date_booked')

    #Recent booking (latest)
    recent_booking = bookings.first()

 #   #Get rooms already booked by this user
    booked_rooms = Booking.objects.filter(
        user=user,
        status='pending'
    ).values_list('room_id', flat=True)

    #Filter rooms by gender (CRITICAL UX FIX) #will be right back
    user_gender = request.user.profile.gender
    rooms = Room.objects.filter(gender=user_gender)

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
    messages.info(request, "Room request has been cancelled!")    
    return redirect('dashboard')

@login_required
def room_view(request):
    rooms = Room.objects.all()
    return render(request, 'core/rooms.html', {'rooms': rooms})

@login_required
def profile_view(request):
    user = request.user
    profile = user.profile  # or user.profile

    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        phone_number = request.POST.get("phone_number")

        #profile settings
        profile_picture = request.FILES.get("profile_picture")
        if profile_picture:
            profile.profile_picture = profile_picture
            profile.save()

        #Phone number must be numbers
        if not phone_number.isdigit():
         messages.error(request, "Phone must be numeric.")

        #Phone number can't be empty
        if phone_number == '':
            messages.error(request, "Phone number can't be empty")
            return redirect('profile')

        #Username can't be empty
        if not username:
         messages.error(request, "Username cannot be empty.")

        #VALIDATION
        if CustomUser.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('profile')

        #Update User
        user.username = username
        user.first_name = first_name
        user.save()

        #Update Profile
        profile.phone_number = phone_number
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'core/profile.html', {
        'user': user,
        'profile': profile
    })
