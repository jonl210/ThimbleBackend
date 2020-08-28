from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateUserSerializer, ResultProfileSerializer, ProfileTabSerializer
from .models import Profile
from groups.models import Group
from groups.serializers import GroupSerializer
from posts.models import Post
from posts.serializers import PostSerializer
from likes.models import Like

from notifications.models import Notification

from google.cloud import storage

storage_client = storage.Client()
media_bucket = storage_client.get_bucket("thimble-media-store")

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
    if group_type == "created":
        groups = profile.groups.all()
    elif group_type == "joined":
        groups = profile.joined_groups.all().exclude(creator=profile)

    groups_serializer = GroupSerializer(groups, many=True)
    return Response(groups_serializer.data)

# Return info for user profile
@api_view(['GET'])
def profile(request):
    profile = Profile.objects.get(user=request.user)
    profile_serializer = ProfileTabSerializer(profile)
    return Response(profile_serializer.data)

# Update profile info
@api_view(['POST'])
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.data["photo"] != None:
        photo_u_id = Post().generate_post_id()
        photo_url = upload_profile_photo(request.data["photo"], photo_u_id)
        profile.profile_picture = photo_url
        profile.save()
        return Response(status=status.HTTP_200_OK)

def upload_profile_photo(photo, u_id):
    blob = media_bucket.blob(u_id)
    blob.upload_from_file(photo, content_type="image/jpeg")
    blob.make_public()
    return blob.public_url

# Return all users posts
@api_view(['GET'])
def posts(request):
    profile = Profile.objects.get(user=request.user)
    profile_posts = profile.my_posts.all()
    posts = []
    for post in profile_posts:
        like_count = post.post_likes.count()
        if Like.objects.filter(post=post, profile=profile).exists():
            posts.append({"post": PostSerializer(post).data, "is_liked": "true", "like_count": like_count})
        else:
            posts.append({"post": PostSerializer(post).data, "is_liked": "false", "like_count": like_count})
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
        like_count = post.post_likes.count()
        if Like.objects.filter(post=post, profile=profile).exists():
            posts.append({"post": PostSerializer(post).data, "is_liked": "true", "like_count": like_count})
        else:
            posts.append({"post": PostSerializer(post).data, "is_liked": "false", "like_count": like_count})
    return Response(posts)
