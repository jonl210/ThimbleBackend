from django.urls import path

from . import views

from rest_framework.authtoken import views as rest_views

app_name = 'users'
urlpatterns = [
    path('search/', views.search),
    path('token', rest_views.obtain_auth_token),
    path('', views.register_user),
    path('groups/created', views.created_groups),
]
