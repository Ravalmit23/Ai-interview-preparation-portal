from django.urls import path
from . import views

urlpatterns = [
    path('interview/', views.interview, name='interview'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
]