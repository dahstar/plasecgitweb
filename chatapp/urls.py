from django.urls import path
from .views import chat_view
from chatapp.views import delete_message,play_in_telegram

app_name = 'chatapp'

urlpatterns = [
    path('', chat_view, name='chat'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
     path('play_in_telegram/',  play_in_telegram, name='play_in_telegram'),

]
