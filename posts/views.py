from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer
from .models import Post, PhotoMedia
from groups.models import Group
from users.models import Profile

from google.cloud import storage

storage_client = storage.Client()
media_bucket = storage_client.get_bucket("thimble-media-store")

@api_view(['POST'])
def create_photo_post(request):
    photo = request.data["photo"]
    u_id = Post().generate_post_id()
    blob = media_bucket.blob(u_id)
    blob.upload_from_file(photo, content_type="image/jpeg")
    blob.make_public()
    return Response(status=status.HTTP_201_CREATED)
