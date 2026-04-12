from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

#model for custom user
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    def __str__(self):
       return f"{self.username} ({self.role})"



#model for main user
class MainUser(models.Model):
   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
   first_name = models.CharField(max_length=50)
   last_name = models.CharField(max_length=50)
   gender = models.CharField(max_length=10, choices=[('male','Male'), ('female','Female')])
   phone_number = models.IntegerField()
   profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/blank_profile_picture.png', blank=True, null=True)

   def __str__(self):
       return f"{self.first_name} {self.last_name} - {self.phone_number} - {self.profile_picture}"


#model for room
class Room(models.Model):
   room_number = models.CharField(max_length=20)
   capacity = models.IntegerField()
   gender = models.CharField(max_length=20, choices=[('male','Male'),('female', 'Female')], default='male')

   def __str__(self):
      return f"{self.room_number}, {self.capacity}, {self.gender}"

#model for booking
class Booking(models.Model):
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='booking')
   room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='booking')
   date_booked = models.DateTimeField(auto_now_add=True)
   status = models.CharField(max_length=10,choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending')
   
   class Meta:
      unique_together = ("user", "room", "date_booked", "status")
    
   def __str__(self):
       return f"{self.user},{self.room},{self.date_booked},{self.status}"
   

   #changing the customUser to user to avoid collion and error that i will come accross
