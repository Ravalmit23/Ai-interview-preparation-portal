from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [

    # Admin
    path(
        'admin/',
        admin.site.urls
    ),

    # Home
    path(
        '',
        views.index,
        name='index'
    ),

    # Authentication
    path(
        'login/',
        views.login,
        name='login'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login2/',
        views.login2,
        name='login2'
    ),

    # Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # Practice
    path(
        'practice/',
        views.practice,
        name='practice'
    ),

    # Feature
    path(
        'feature/',
        views.feature,
        name='feature'
    ),

    # Interview
    path(
        'interview/<str:technology>/',
        views.technology_view,
        name='technology_view'
    ),

    # Submit
    path(
        'submit-answer/',
        views.submit_answer,
        name='submit_answer'
    ),
]