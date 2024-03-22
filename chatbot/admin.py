from django.contrib import admin
from .models import LawyerChatbot

# Register your models here.

@admin.register(LawyerChatbot)
class LawyerChatbotAdmin(admin.ModelAdmin):
    list_display = ('user_input', 'bot_response', 'timestamp')

