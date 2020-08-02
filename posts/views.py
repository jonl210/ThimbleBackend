from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer
from .models import Post, PhotoMedia
from groups.models import Group
from users.models import Profile
from likes.models import Like

from google.cloud import storage

storage_client = storage.Client()
media_bucket = storage_client.get_bucket("thimble-media-store")

@api_view(['POST'])
def create_photo_post(request):
    profile = Profile.objects.get(user=request.user)
    group = Group.objects.get(u_id=request.data["group_u_id"])
    post_u_id = Post().generate_post_id()
    photo_url = upload_photo(request.data["photo"], post_u_id)
    photo_media_object = PhotoMedia.objects.create(url=photo_url, caption=request.data["caption"])
    Post.objects.create(profile=profile, group=group, u_id=post_u_id, post_type=0, photo=photo_media_object)
    return Response(status=status.HTTP_201_CREATED)

def upload_photo(photo, u_id):
    blob = media_bucket.blob(u_id)
    blob.upload_from_file(photo, content_type="image/jpeg")
    blob.make_public()
    return blob.public_url

@api_view(['POST'])
def like_post(request, u_id):
    profile = Profile.objects.get(user=request.user)
    post = Post.objects.get(u_id=u_id)
    if not Like.objects.filter(post=post, profile=profile).exists():
        Like.objects.create(post=post, profile=profile)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_409_CONFLICT)

@api_view(['DELETE'])
def unlike_post(request, u_id):
    profile = Profile.objects.get(user=request.user)
    post = Post.objects.get(u_id=u_id)
    if Like.objects.filter(post=post, profile=profile).exists():
        Like.objects.get(post=post, profile=profile).delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
