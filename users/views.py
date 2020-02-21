from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateUserSerializer, ResultProfileSerializer
from .models import Profile

#Register a new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == "POST":
        user_serializer = CreateUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors)

#Search for users
@api_view(['GET'])
def search(request):
    if request.method == "GET":
        query = request.query_params["search_query"]
        if User.objects.filter(username=query).exists():
            result_profile = Profile.objects.get(user=User.objects.get(username=query))
            result_profile_serializer = ResultProfileSerializer(result_profile)
            return Response(result_profile_serializer.data)
