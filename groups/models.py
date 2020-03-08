from django.db import models

from datetime import datetime

import random, string, os

class Group(models.Model):
    name = models.CharField(max_length=60)
    u_id = models.CharField(max_length=10)
    creator = models.ForeignKey('users.profile', on_delete=models.PROTECT, related_name="groups")
    date = models.DateTimeField(default=datetime.now)
    banner = models.URLField(default="replace")
    members = models.ManyToManyField('users.profile', related_name="joined_groups")

    def generate_group_id(self):
        unique = False
        random_id = 0

        #Check if id already exists
        while not unique:
            random_id = ''.join([random.choice(string.ascii_letters+string.digits) for n in range(10)])
            if Group.objects.filter(u_id=random_id).exists():
                unique = False
            else:
                unique = True
            return random_id
