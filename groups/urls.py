from django.urls import path

from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.create_group),
    path('<u_id>/<username>/<action>', views.edit_group_members),
    path('<u_id>/members', views.members),
    path('<u_id>/non-member-friends', views.non_member_friends),
    path('<u_id>/posts', views.posts),
]
