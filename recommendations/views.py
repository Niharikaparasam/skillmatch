from django.shortcuts import render
from .models import Skill, Recommendation

def index(request):
    skills = Skill.objects.all()
    recommendations = Recommendation.objects.all()
    return render(request, 'home.html', {'skills': skills, 'recommendations': recommendations})

