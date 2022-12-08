from django.db import models
from django.utils import timezone
# Create your models here.

class User(models.Model):
  username = models.CharField(max_length = 10)
  pwd = models.CharField(max_length=20)
  email = models.EmailField()
  ifDriver = models.BooleanField(default=False)
  
  def __str__(self):
    return self.username 

class Vehicle(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="vehicle",null=True)
    vehicle_type = models.CharField(max_length = 10)
    license_num = models.CharField(max_length = 10)
    max_num = models.IntegerField()
    spec_veh_info = models.TextField()
    def __str__(self):
      return self.driver.username + " & " + self.vehicle_type 

class Ride(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="owner",null=True)#one user may have multiple rides
  driver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="driver",null=True)#one user may have multiple rides
  #pub_date名字有改动 
  date_time = models.DateTimeField(default=timezone.now)
  # date = models.DateField(default=timezone.now)
  # time = models.TimeField(default=timezone.now)
  destination = models.TextField(max_length = 200)
  num_of_passenger = models.IntegerField(default=0)
  status = models.CharField(max_length = 10,default = "open")
  ifShared = models.BooleanField()
  spec_ride_req = models.TextField()
  vehicle_type = models.CharField(max_length = 10)
  vehicle_capacity = models.IntegerField(default=0)
  sharer = models.ManyToManyField(User, related_name="sharer", blank=True)
  editable = models.BooleanField(default = True)
  def __str__(self):
    return self.owner.username + " & " + self.destination
    
  # def get_date_str(self):
  #   return self.date.strftime("%Y-%m-%d")

  # def get_time_str(self):
  #   return self.time.strftime("%H:%M")

  def get_date_time_str(self):
    return self.date_time.strftime("%Y-%m-%dT%H:%M")