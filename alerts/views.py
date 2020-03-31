from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import NotificationSerializer
from users.models import Profile

from notifications.signals import notify
from notifications.models import Notification

#Retrieve all unread notifications
@api_view(['GET'])
def inbox(request):
    notifs = request.user.notifications.unread()
    notfis_serializer = NotificationSerializer(notifs, many=True)
    return Response(notfis_serializer.data)

#Send friend request notification
#from_user is a profile object to get profile picture
@api_view(['POST'])
def send_friend_request(request, username):
    to_user = User.objects.get(username=username)
    from_profile = Profile.objects.get(user=request.user)
    notify.send(sender=from_profile, recipient=to_user, verb="friend request")
    return Response(status=status.HTTP_201_CREATED)

#Delete friend request after adding friend or not
@api_view(['PUT', 'DELETE'])
def edit_friend_request(request, username):
    from_profile = Profile.objects.get(user=User.objects.get(username=username))
    to_profile = Profile.objects.get(user=request.user)

    if request.method == "PUT":
        to_profile.friends.add(from_profile)

    Notification.objects.get(actor_object_id=from_profile.id, recipient=to_profile.user, verb="friend request").delete()
    return Response(status=status.HTTP_200_OK)
