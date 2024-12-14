# recommendations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('recommend_courses/', views.recommend_courses, name='recommend_courses'),
]
