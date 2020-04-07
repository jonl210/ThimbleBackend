from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateUserSerializer, ResultProfileSerializer
from .models import Profile
from groups.models import Group
from groups.serializers import GroupSerializer

from notifications.models import Notification

#Register a new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    user_serializer = CreateUserSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        new_user_profile = user_serializer.save()

        #Check if full name was provided
        if request.data.get("full_name", None) != None:
            new_user_profile.full_name = request.data["full_name"]
            new_user_profile.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(user_serializer.errors)

#Search for users
@api_view(['GET'])
def search(request):
    query = request.query_params["search_query"]
    if User.objects.filter(username=query).exists():
        result_user = User.objects.get(username=query)
        searcher_profile = Profile.objects.get(user=request.user)
        result_profile = Profile.objects.get(user=result_user)
        result_profile_serializer = ResultProfileSerializer(result_profile)

        if Notification.objects.filter(actor_object_id=searcher_profile.id, recipient=result_user, verb="friend request").exists():
            return Response({"status": "pending", "result": result_profile_serializer.data})
        elif searcher_profile.friends.all().filter(user=result_profile.user).exists():
            return Response({"status": "friends", "result": result_profile_serializer.data})
        elif searcher_profile == result_profile:
            return Response({"status": "you", "result": result_profile_serializer.data})

        return Response(result_profile_serializer.data)
    else:
        return Response({"result": "user not found"})

#Get groups based on type
@api_view(['GET'])
def groups(request, group_type):
    profile = Profile.objects.get(user=request.user)
    groups = 0
    if group_type == "created":
        groups = profile.groups.all()
    elif group_type == "joined":
        groups = profile.joined_groups.all()

    groups_serializer = GroupSerializer(groups, many=True)
    return Response(groups_serializer.data)
