from django.db import models

# Create your models here.

class LawyerChatbot(models.Model):
    user_input = models.TextField()  # 사용자 입력
    bot_response = models.TextField()  # 챗봇 응답
    timestamp = models.DateTimeField(auto_now_add=True)  # 타임스탬프
    def __str__(self):
        return f"User: {self.user_input} - Bot: {self.bot_response}"
