from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Group
from users.models import Profile
from .serializers import CreateGroupSerializer
from users.serializers import BasicProfileSerializer

#Create a new group
@api_view(['POST'])
def create_group(request):
    group_serializer = CreateGroupSerializer(data=request.data)
    if group_serializer.is_valid():
        group_serializer.save(creator=Profile.objects.get(user=request.user))
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(group_serializer.errors)

#Add or remove profile from group
@api_view(['PUT'])
def edit_group_members(request, u_id, action, username):
    member_profile = Profile.objects.get(user=User.objects.get(username=username))
    group = Group.objects.get(u_id=u_id)

    if action == "add":
        group.members.add(member_profile)
    elif action == "remove":
        group.members.remove(member_profile)

    return Response(status=status.HTTP_200_OK)

#Return members in a group
@api_view(['GET'])
def members(request, u_id):
    group = Group.objects.get(u_id=u_id)
    members = group.members.all()
    members_serializer = BasicProfileSerializer(members, many=True)
    return Response(members_serializer.data)

#Return friends not in a group
@api_view(['GET'])
def non_member_friends(request, u_id):
    profile = Profile.objects.get(user=request.user)
    group = Group.objects.get(u_id=u_id)
    friends = profile.friends.all()
    members = group.members.all()

    #Check if friends are already members
    if members.count() != 0:
        for member in members:
            friends = friends.exclude(user=member.user)

    friends_serializer = BasicProfileSerializer(friends, many=True)
    return Response(friends_serializer.data)
