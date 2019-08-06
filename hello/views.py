from django.shortcuts import render
from django.http import HttpResponse

from .models import Component

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, "db.html", {"greetings": greetings})


def db(request):

    component = Component(name="1", version_nuumber="1.1", date="04.08.2019", url="www.google.com")
    component.save()

    components = component.objects.all()

    return render(request, "db.html", {"components": components})