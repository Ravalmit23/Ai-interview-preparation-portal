from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')

def admin(request):
    return render(request, 'login2.html')

def feature(request):
    return render(request,'feature.html')


# @login_required(login_url='login')
def practice(request):
    return render(request, 'practice.html')