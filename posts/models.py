from django.db import models

from datetime import datetime

import random, string, os

class PhotoMedia(models.Model):
    url = models.URLField()
    caption = models.TextField()

class LinkMedia(models.Model):
    url = models.URLField()
    description = models.TextField()

class Post(models.Model):
    class PostType(models.IntegerChoices):
        PHOTO = 0
        LINK = 1
        TEXT = 2
    profile = models.ForeignKey('users.profile', on_delete=models.PROTECT, related_name="my_posts")
    group = models.ForeignKey('groups.group', on_delete=models.PROTECT, related_name="group_posts")
    date = models.DateTimeField(default=datetime.now)
    u_id = models.CharField(max_length=20, default="replace")
    post_type = models.IntegerField(PostType.choices)
    photo = models.OneToOneField(PhotoMedia, on_delete=models.CASCADE, blank=True, null=True)
    link = models.OneToOneField(LinkMedia, on_delete=models.CASCADE, blank=True, null=True)
