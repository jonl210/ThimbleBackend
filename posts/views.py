from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer
from .models import Post
from users.models import Profile
from likes.models import Like

from . import PostsHelper

@api_view(['POST'])
def create_photo_post(request):
    PostsHelper.create_post(request.data, request.user, Post.PostType.PHOTO)
    return Response(status=status.HTTP_201_CREATED)

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
