from rest_framework import serializers

from .models import Group

# Create new group and validate name
class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'description']

    # Create group from posted name, creator passed from view
    def create(self, validated_data):
        name = validated_data["name"]
        description = validated_data["description"]
        u_id = Group().generate_group_id()
        group = Group.objects.create(name=name, description=description, u_id=u_id, creator=validated_data["creator"])
        return group

# Field to return member field count
class MemberCountField(serializers.Field):
    def to_representation(self, value):
        return value.all().count()

class GroupSerializer(serializers.ModelSerializer):
    members = MemberCountField()

    class Meta:
        model = Group
        exclude = ['id', 'creator', 'date', 'description']
