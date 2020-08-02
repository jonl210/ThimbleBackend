from django.db import models
from datetime import datetime

class Like(models.Model):
    post = models.ForeignKey('posts.post', on_delete=models.CASCADE, related_name="post_likes")
    profile = models.ForeignKey('users.profile', on_delete=models.CASCADE, related_name="user_likes")
    date = models.DateTimeField(default=datetime.now)
