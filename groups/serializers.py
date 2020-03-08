from rest_framework import serializers

from .models import Group
from users.models import Profile

#Create new group and validate name
class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

    #Create group from posted name, creator passed from view
    def create(self, validated_data):
        name = validated_data["name"]
        u_id = Group().generate_group_id()
        group = Group.objects.create(name=name, u_id=u_id, creator=validated_data["creator"])
        return group
