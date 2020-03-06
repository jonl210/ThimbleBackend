from django.urls import path

from . import views

app_name = 'alerts'
urlpatterns = [
    path('inbox', views.inbox),
    path('<username>/friend', views.send_friend_request),
    path('<username>/accept', views.accept_friend_request),
    path('<username>/delete', views.delete_friend_request),
]
