# recommendations/views.py
from django.shortcuts import render
from .recommendations_logic import get_knn_recommendations

def recommend_courses(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        if student_name:
            get_knn_recommendations(students_df, courses_df, previous_courses_df, student_name)
        else:
            print("Please enter a valid student name.")
    return render(request, 'recommendations/recommend_courses.html')
