from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def chat(request):
    return HttpResponse("Test")
