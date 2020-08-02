from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('photo', views.create_photo_post),
    path('<u_id>/like', views.like_post),
    path('<u_id>/unlike', views.unlike_post),
]
