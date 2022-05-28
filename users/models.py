from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    city = models.CharField(max_length=100, null=True)
    is_online = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='images/')
