from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.TextField()
    profile_pic = models.ImageField()
    def __str__(self):
        return str(self.username)
    

class WeatherData(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,default=0)
    city = models.CharField(max_length=100)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    weather=models.CharField(max_length=10,default=0)
    speed=models.CharField(max_length=10,default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Weather in {self.city} at {self.timestamp}"