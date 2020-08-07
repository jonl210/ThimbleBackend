from django.db import models
from django.contrib.auth.models import User

from django_mysql.models import ListTextField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=70, blank=True)
    profile_picture = models.URLField(blank=True)
    friends = models.ManyToManyField("self")
    feed = ListTextField(base_field=models.CharField(max_length=20), blank=True, null=True)
