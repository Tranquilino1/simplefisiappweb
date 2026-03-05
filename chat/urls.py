from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('chat/<str:room_name>/upload/', views.upload_attachment, name='upload_attachment'),
]
