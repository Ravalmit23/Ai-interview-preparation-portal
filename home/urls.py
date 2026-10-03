from django.urls import path
from . import views

urlpatterns = [
    path('interview/', views.technology_view, name='technology_view'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
]