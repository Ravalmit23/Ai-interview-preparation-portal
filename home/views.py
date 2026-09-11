from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Question
from django.shortcuts import render,redirect
from django.conf import settings
import os
from openai import OpenAI
from django.shortcuts import render,redirect
from dotenv import load_dotenv
load_dotenv()

def get_openai_client():
    if not settings.OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY is not configured.')
    return OpenAI(api_key=settings.OPENAI_API_KEY)


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
        client = get_openai_client()

        question_id = request.POST.get('question_id')
        answer = request.POST.get('answer')
        technology = request.POST.get('technology')

        question = Question.objects.get(id=question_id)

        response = client.responses.create(
            model="gpt-5.6-mini",
            input=f"""
You are an interviewer evaluating a student's technical interview answer.

Technology: {technology}

Question:
{question.question}
Student's answer:
{answer}

Evaluate the answer and give:
1. Score out of 10
2. What was correct
3. What was missing or incorrect
4. How the student can improve

Keep the feedback clear and suitable for a student.
"""
        )

        feedback = response.output_text

        print("AI FEEDBACK:")
        print(feedback)

        return render(request, 'result.html', {
            'question': question,
            'answer': answer,
            'feedback': feedback,
            'technology': technology
        })

    return redirect('practice')