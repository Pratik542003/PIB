from django.urls import path
from . import views
from .views import approve_video, edit_video

urlpatterns = [
    path('index', views.index, name='index'),
    path('ApprovedVideo', views.ApprovedVideo, name='ApprovedVideo'),
    path('PendingVideo', views.PendingVideo, name='PendingVideo'),
    path('Login', views.Login, name='Login'),
    path('Register', views.Register, name='Register'),
    path('', views.InputPage, name='InputPage'),
    path('InputPage', views.InputPage, name='InputPage'),
    path('edit', views.edit, name='edit'),
    path('videos', views.video_list, name='video_list'),
    path('videos/call_function/<int:video_id>/', approve_video, name='approve_video'),
    path('videos/view/<int:video_id>/', edit_video, name='edit_video'),
]
