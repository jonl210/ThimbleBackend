from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Group
from users.models import Profile
from .serializers import CreateGroupSerializer
from users.serializers import BasicProfileSerializer, ResultProfileSerializer

from posts import PostsHelper
from posts.models import Post

from notifications.signals import notify
from notifications.models import Notification

# Create a new group
@api_view(['POST'])
def create_group(request):
    group_serializer = CreateGroupSerializer(data=request.data)
    if group_serializer.is_valid():
        group = group_serializer.save(creator=Profile.objects.get(user=request.user))

        # Add creator as a member
        group.members.add(Profile.objects.get(user=request.user))

        if request.data.get("photo", None) != None:
            photo_u_id = Post.generate_post_id()
            photo_url = PostsHelper.upload_photo(request.data["photo"], photo_u_id)
            group.banner = photo_url
            group.save()

        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(group_serializer.errors)

# Add or remove profile from group
@api_view(['PUT'])
def edit_group_members(request, u_id, action, username):
    member_profile = Profile.objects.get(user=User.objects.get(username=username))
    group = Group.objects.get(u_id=u_id)

    if action == "add":
        group.members.add(member_profile)
        from_profile = Profile.objects.get(user=request.user)
        verb = "added you to the group {}".format(group.name)

        # Check if notification already exists
        if not Notification.objects.filter(actor_object_id=from_profile.id, recipient=member_profile.user, verb=verb).exists():
            notify.send(sender=from_profile, recipient=member_profile.user, verb=verb)
    elif action == "remove":
        group.members.remove(member_profile)

    return Response(status=status.HTTP_200_OK)

# Return members in a group
@api_view(['GET'])
def members(request, u_id):
    group = Group.objects.get(u_id=u_id)
    members = group.members.all().exclude(user=group.creator.user)
    members_serializer = BasicProfileSerializer(members, many=True)
    return Response(members_serializer.data)

# Return friends not in a group
@api_view(['GET'])
def non_member_friends(request, u_id):
    profile = Profile.objects.get(user=request.user)
    group = Group.objects.get(u_id=u_id)
    friends = profile.friends.all()
    members = group.members.all()

    # Check if friends are already members
    if members.count() != 0:
        for member in members:
            friends = friends.exclude(user=member.user)

    friends_serializer = BasicProfileSerializer(friends, many=True)
    return Response(friends_serializer.data)

# Return all posts in a group
@api_view(['GET'])
def posts(request, u_id):
    group = Group.objects.get(u_id=u_id)
    group_posts = group.group_posts.all().order_by("-date")
    profile = Profile.objects.get(user=request.user)
    posts = []
    for post in group_posts:
        posts.append(PostsHelper.set_like_status(post, profile))
    return Response(posts)

# Return current members in a group
@api_view(['GET'])
def current_members(request, u_id):
    group = Group.objects.get(u_id=u_id)
    members = group.members.all()
    members_serializer = ResultProfileSerializer(members, many=True)
    return Response(members_serializer.data)
