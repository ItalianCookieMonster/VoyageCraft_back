# chatbot/urls.py

from django.urls import path
from .views import get_bot_response

urlpatterns = [
    path('get-response/', get_bot_response, name='get_bot_response'),
]
