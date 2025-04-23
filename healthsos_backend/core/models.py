from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    blood_type = models.CharField(max_length=3, blank=True)
    chronic_conditions = models.TextField(blank=True)

class SOSRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location_lat = models.FloatField()
    location_lng = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

