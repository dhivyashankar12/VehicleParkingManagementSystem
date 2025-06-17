from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    categoryname = models.CharField(max_length=50)
    slot_count = models.PositiveIntegerField(default=0)  
    current_slot = models.IntegerField(default=0)


    def __str__(self):
        return self.categoryname



class Vehicle(models.Model):
    id = models.BigAutoField(primary_key=True)
    parkingnumber = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vehiclecompany = models.CharField(max_length=50)
    regno = models.CharField(max_length=10)
    ownername = models.CharField(max_length=50)
    ownercontact = models.CharField(max_length=15)
    pdate = models.DateField()
    intime = models.DateTimeField()
    outtime = models.DateTimeField(null=True, blank=True)
    parkingcharge = models.CharField(max_length=50)
    remark = models.CharField(max_length=500)
    status = models.CharField(max_length=20)
    def __str__(self):
        return self.parkingnumber

class ParkingSlot(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    total_slots = models.PositiveIntegerField()
    occupied_slots = models.PositiveIntegerField(default=0)

    def available_slots(self):
        return self.total_slots - self.occupied_slots

    def __str__(self):
        return f"{self.category.categoryname} Slots"


