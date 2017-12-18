from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    status = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username





