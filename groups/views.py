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

#Add friend to specific group
@api_view(['PUT'])
def add_friend_to_group(request, u_id, username):
    friend_profile = Profile.objects.get(user=User.objects.get(username=username))
    group = Group.objects.get(u_id=u_id)
    group.members.add(friend_profile)
    return Response(status=status.HTTP_200_OK)
