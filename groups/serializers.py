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

# Field to return username from creator field
class CreatorField(serializers.Field):
    def to_representation(self, value):
        return (value.user.username, value.profile_picture)

# Field to return member field count
class MemberCountField(serializers.Field):
    def to_representation(self, value):
        return value.all().count()

# Field to format date
class DateField(serializers.Field):
    def to_representation(self, value):
        return value.strftime("%b %-d, %Y")

class GroupSerializer(serializers.ModelSerializer):
    creator = CreatorField()
    members = MemberCountField()
    date = DateField()

    class Meta:
        model = Group
        exclude = ['id']
