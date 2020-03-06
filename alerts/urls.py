from django.urls import path

from . import views

app_name = 'alerts'
urlpatterns = [
    path('inbox', views.inbox),
    path('<username>/friend', views.send_friend_request),
]
