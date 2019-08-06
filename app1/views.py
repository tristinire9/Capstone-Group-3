from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return HttpResponse("app1 index text")


def page1(request):
    return HttpResponse("page1 text")

def page2(request):
    return HttpResponse("page2 text")