from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def page1(request):
    return HttpResponse("page1 text")

def page2(request):
    return HttpResponse("page2 text")