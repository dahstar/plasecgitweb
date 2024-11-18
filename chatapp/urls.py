from django.urls import path
from .views import chat_view
from chatapp.views import delete_message,trigger_start,message_clicked
from . import views

app_name = 'chatapp'

urlpatterns = [
    path('', chat_view, name='chat'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('message_clicked/<int:message_id>/', message_clicked, name='delete_message'),
    path('play_in_telegram/<str:message_id>/', views.play_in_telegram, name='play_in_telegram'),
         path('trigger_start/', trigger_start, name='trigger_start'),


]
