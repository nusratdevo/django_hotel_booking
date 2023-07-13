from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse


class Facilities(models.Model):
    name=models.CharField(max_length=100)
    is_available=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Rooms(models.Model):
    room_no=models.CharField(max_length=5)
    room_type=models.CharField(max_length=50)
    is_available=models.BooleanField(default=True)
    price=models.FloatField(default=1000.00)
    no_of_days_advance=models.IntegerField()
    start_date=models.DateField(auto_now=False, auto_now_add=False)
    room_image=models.ImageField(upload_to="media", max_length=None, default='0.jpeg')
    facilites_no=models.ManyToManyField(Facilities)

    def __str__(self):
        return "Room No: "+str(self.id)
   
    def get_url(self):
        return reverse('room_detail', args=[self.id])
  

class RoomImage(models.Model):
    room=models.ForeignKey(Rooms, on_delete=models.CASCADE)
    room_image=models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None)


class Booking(models.Model):
    room_no=models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    start_day=models.DateField(auto_now=False, auto_now_add=False)
    end_day=models.DateField(auto_now=False, auto_now_add=False)
    price=models.FloatField()
    no_of_days=models.IntegerField()
    booked_on=models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return "Booking ID: "+str(self.id)
    @property
    def is_past_due(self):
        return date.today()>self.end_day


