from django.db import models

from datetime import datetime

class Group(models.Model):
    name = models.CharField(max_length=60)
    u_id = models.CharField(max_length=10)
    creator = models.ForeignKey('users.profile', on_delete=models.PROTECT, related_name="groups")
    date = models.DateTimeField(default=datetime.now)
