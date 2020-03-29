from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Group
from users.models import Profile
from .serializers import CreateGroupSerializer

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
