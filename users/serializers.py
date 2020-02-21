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

    #Check if username is taken
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use")
        else:
            return value

    #Check if email is taken
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        else:
            return value

    #Create new user, profile and auth token
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        Token.objects.create(user=user)
        return user

#Serializers for searching
class ResultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ResultProfileSerializer(serializers.ModelSerializer):
    user = ResultUserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture']
