from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User
from .models import LawyerChatBot
from django.utils import timezone
import os
from dotenv import load_dotenv

load_dotenv()
# OPENAI API KEY : 버전 관리에는 절대 넣지 마세요.
openai.api_key = os.getenv("OPENAI_API_KEY")


# api 응답 함수
def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    # print(response)
    answer = response.choices[0].message.content.strip()
    return answer


def chatbot(request):
    chats = LawyerChatBot.objects.filter(user=request.user.id)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        # 응답 db 저장
        chat = LawyerChatBot(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})


# 로그인
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # 권한 확인
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = '닉네임 또는 비밀번호가 틀렸습니다.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


# 회원가입
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save() # db 저장
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = '계정 생성에 실패했습니다.'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = '비밀번호가 틀렸습니다.'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')


# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('chatbot')