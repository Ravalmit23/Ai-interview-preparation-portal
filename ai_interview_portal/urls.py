from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('login2/', views.login2, name='login2'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('practice/', views.practice, name='practice'),
    path('feature/', views.feature, name='feature'),

    path(
        'interview/<str:technology>/',
        views.technology_view,
        name='technology_view'
    ),

    path(
        'submit-answer/',
        views.submit_answer,
        name='submit_answer'
    ),
]