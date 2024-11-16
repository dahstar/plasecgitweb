from django.urls import path
from .views import chat_view
from . import views

app_name = 'chatapp'

urlpatterns = [
    path('', chat_view, name='chat'),
    path('message_clicked/<int:message_id>/', views.message_clicked, name='message_clicked'),
    path('get_blockchain/', views.get_blockchain, name='get_blockchain'),
]
