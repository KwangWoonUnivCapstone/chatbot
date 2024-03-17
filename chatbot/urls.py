from django.urls import path
from .views import hello

app_name = 'chatbot'

urlpatterns = [
    path("", hello),
]