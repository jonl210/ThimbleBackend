from django.urls import path

from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.create_group),
    path('<u_id>/add/<username>', views.add_friend_to_group),
]
