from rest_framework import serializers

from notifications.models import Notification

from users.serializers import ResultProfileSerializer

#Serializer for all notifications
class NotificationSerializer(serializers.ModelSerializer):
    actor = ResultProfileSerializer()

    class Meta:
        model = Notification
        fields = ['actor', 'verb']
