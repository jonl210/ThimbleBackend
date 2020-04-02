from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=70, blank=True)
    profile_picture = models.URLField(default="replace")
    friends = models.ManyToManyField("self")
