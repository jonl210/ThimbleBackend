from likes.models import Like
from .serializers import PostSerializer
from .models import Post, PhotoMedia
from users.models import Profile
from groups.models import Group
from likes.models import Like

from google.cloud import storage

from django_mysql.models import ListF

import os
from datetime import datetime, timedelta

storage_client = storage.Client()
media_bucket = storage_client.get_bucket(os.environ["MEDIA_BUCKET"])

def create_post(data, user, type):
    profile = Profile.objects.get(user=user)
    group = Group.objects.get(u_id=data["group_u_id"])
    post_u_id = Post.generate_post_id()
    photo_url = upload_photo(data["photo"], post_u_id)
    photo_media_object = PhotoMedia.objects.create(url=photo_url, caption=data["caption"])
    Post.objects.create(profile=profile, group=group, u_id=post_u_id, post_type=type, photo=photo_media_object)
    group_members = group.members.all()
    deliver_post_id(post_u_id, group_members)

def prepare_post(post, profile):
    post_like_status = set_like_status(post, profile)
    post_time_elapsed = get_time_elapsed(post)
    return {"post": PostSerializer(post).data, "is_liked": post_like_status[0], "like_count": post_like_status[1],\
            "time_elapsed": post_time_elapsed}

def get_time_elapsed(post):
    post_time = post.date
    time_difference = datetime.now() - post_time
    elapsed_time = ('','')
    if time_difference.total_seconds() // 604800 < 4:
        elapsed_time = (time_difference.total_seconds() // 604800, 'w')
    elif time_difference.total_seconds() // 86400 < 7:
        elapsed_time = (time_difference.total_seconds() // 86400, 'd')
    elif time_difference.total_seconds() // 3600 < 24:
        elapsed_time = (time_difference.total_seconds() // 3600, 'h')
    elif time_difference.total_seconds() // 60 < 60:
        elapsed_time = (time_difference.total_seconds() // 60, 'm')
    elif time_difference.total_seconds() < 60:
        elapsed_time = (time_difference.total_seconds(), 's')
    else:
        return post_time.strftime("%b %-d, %Y")
    return f'{int(elapsed_time[0])}{elapsed_time[1]}'

def set_like_status(post, profile):
    is_liked = "false"
    if Like.objects.filter(post=post, profile=profile).exists():
        is_liked = "true"
    return (is_liked, post.post_likes.count())

def upload_photo(photo, u_id):
    blob = media_bucket.blob(u_id)
    blob.upload_from_file(photo, content_type="image/jpeg")
    blob.make_public()
    return blob.public_url

def deliver_post_id(post_id, group_members):
    for member in group_members:
        Profile.objects.filter(user=member.user).update(feed=ListF('feed').appendleft(post_id))
