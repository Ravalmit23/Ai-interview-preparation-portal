from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Question
from django.shortcuts import render,redirect


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
def interview(request, technology):
    questions = Question.objects.filter(
        technology=technology
    )

    return render(request, 'interview.html', {
        'questions': questions,
        'technology': technology
    })
def submit_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer = request.POST.get('answer')

        print(question_id)
        print(answer)

    return redirect('practice')