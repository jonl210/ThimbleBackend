from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PostSerializer
from .models import Post
from groups.models import Group
