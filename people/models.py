from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=2)