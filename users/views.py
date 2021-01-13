from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateUserSerializer, ResultProfileSerializer, ProfileTabSerializer, UpdateProfileSerializer
from .models import Profile
from groups.models import Group
from groups.serializers import GroupSerializer
from posts.models import Post
from posts.serializers import PostSerializer
from likes.models import Like
from posts import PostsHelper

from notifications.models import Notification

from google.cloud import storage

import os

# Register a new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    user_serializer = CreateUserSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        new_user_profile = user_serializer.save()

        # Check if full name was provided
        if request.data.get("full_name", None) != None:
            new_user_profile.full_name = request.data["full_name"]
            new_user_profile.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(user_serializer.errors)

# Search for users
@api_view(['GET'])
def search(request, search_query):
    query = search_query
    results = User.objects.filter(username__icontains=query)
    searcher_profile = Profile.objects.get(user=request.user)
    result_profiles = []
    if results.count() != 0:
        for result in results:
            result_user = User.objects.get(username=result)
            result_user_profile = Profile.objects.get(user=result_user)

            if Notification.objects.filter(actor_object_id=searcher_profile.id, recipient=result_user, verb="friend request").exists():
                result_profiles.append({"status": "pending", "profile": ResultProfileSerializer(result_user_profile).data})
            elif searcher_profile.friends.all().filter(user=result_user).exists():
                result_profiles.append({"status": "friends", "profile": ResultProfileSerializer(result_user_profile).data})
            elif searcher_profile == result_user_profile:
                result_profiles.append({"status": "you", "profile": ResultProfileSerializer(result_user_profile).data})
            else:
                result_profiles.append({"profile": ResultProfileSerializer(result_user_profile).data})
        return Response(result_profiles)
    else:
        return Response({"status": "No results found"})

# Get groups based on type
@api_view(['GET'])
def groups(request, group_type):
    profile = Profile.objects.get(user=request.user)
    groups = 0
    group_array = []
    if group_type == "created":
        groups = profile.groups.all()
    elif group_type == "joined":
        groups = profile.joined_groups.all().exclude(creator=profile)
    groups_serializer = GroupSerializer(groups, many=True)
    for group in groups:
        group_array.append({"group": GroupSerializer(group).data, "posts": group.group_posts.all().count()})
    return Response(group_array)

# Return info for user profile
@api_view(['GET', 'PUT'])
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "GET":
        profile_serializer = ProfileTabSerializer(profile)
        return Response(profile_serializer.data)
    elif request.method == "PUT":
        update_profile_serializer = UpdateProfileSerializer(profile, data=request.data)
        if update_profile_serializer.is_valid():
            update_profile_serializer.save()
            return Response(status=status.HTTP_200_OK)

# Called if profile photo was changed
@api_view(['POST'])
def update_profile_photo(request):
    profile = Profile.objects.get(user=request.user)
    photo_u_id = Post.generate_post_id()
    photo_url = PostsHelper.upload_photo(request.data["photo"], photo_u_id)
    profile.profile_picture = photo_url
    profile.save()
    return Response(status=status.HTTP_200_OK)

# Return all users posts
@api_view(['GET'])
def posts(request):
    profile = Profile.objects.get(user=request.user)
    profile_posts = profile.my_posts.all().order_by("-date")
    posts = []
    for post in profile_posts:
        posts.append(PostsHelper.set_like_status(post, profile))
    return Response(posts)

# Return all users friends
@api_view(['GET'])
def friends(request):
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()
    friends_serializer = ResultProfileSerializer(friends, many=True)
    return Response(friends_serializer.data)

# Return posts in feed
@api_view(['GET'])
def feed(request):
    profile = Profile.objects.get(user=request.user)
    feed_length = 0
    if profile.feed != None:
        feed_length = len(profile.feed)
    posts = []
    for count in range(feed_length):
        post = Post.objects.get(u_id=profile.feed[count])
        posts.append(PostsHelper.set_like_status(post, profile))
    return Response(posts)

# Return users likes
@api_view(['GET'])
def likes(request):
    profile = Profile.objects.get(user=request.user)
    likes = profile.user_likes.all().order_by("-date")
    liked_posts = []
    for like in likes:
        liked_posts.append(PostsHelper.set_like_status(like.post, profile))
    return Response(liked_posts)
