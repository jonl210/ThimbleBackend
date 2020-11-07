from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from .models import Profile

# Create new user and validate data
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6)
    username = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    # Check if username is taken
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use")
        else:
            return value

    # Check if email is taken
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        else:
            return value

    # Create new user, profile and auth token
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        new_profile = Profile.objects.create(user=user)
        Token.objects.create(user=user)
        return new_profile

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'profile_picture']

    def update_profile(self, validated_data):
        self.full_name = validated_data['full_name']

class UsernameField(serializers.Field):
    def to_representation(self, value):
        return value.username

class ProfileTabSerializer(serializers.ModelSerializer):
    user = UsernameField()

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'full_name']

class UsernameForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ResultProfileSerializer(serializers.ModelSerializer):
    user = UsernameForUserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'full_name']

class BasicProfileSerializer(serializers.ModelSerializer):
    user = UsernameForUserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture']
