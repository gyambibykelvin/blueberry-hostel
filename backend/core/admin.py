from django.contrib import admin
from .models import CustomUser, MainUser, Booking, Room
# Register your models here.

class customuser(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'password', 'email', 'role' )

class mainuser(admin.ModelAdmin):
    list_display= ('user', 'first_name', 'last_name', 'gender', 'phone_number', 'profile_picture')

class room(admin.ModelAdmin):
    list_display = ('room_number', 'capacity', 'gender')

class booking(admin.ModelAdmin):
    list_display = ('user', 'room', 'status', 'date_booked')


admin.site.register(CustomUser, customuser)
admin.site.register(MainUser, mainuser)
admin.site.register(Room, room)
admin.site.register(Booking, booking)
