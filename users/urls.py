from django.urls import path

from . import views

from rest_framework.authtoken import views as rest_views

app_name = 'users'
urlpatterns = [
    path('search/<search_query>', views.search),
    path('token', rest_views.obtain_auth_token),
    path('', views.register_user),
    path('groups/<group_type>', views.groups),
    path('profile', views.profile),
    path('profile/update', views.update_profile),
    path('posts', views.posts),
    path('friends', views.friends),
    path('feed', views.feed),
]
