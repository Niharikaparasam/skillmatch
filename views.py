from django.shortcuts import render
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
import random
from .models import Recommendation

# Paths to your datasets
STUDENTS_DATASET = "datasets/Students_Dataset.csv"
COURSES_DATASET = "datasets/Updated_Courses_Dataset.xls"
PREVIOUS_COURSES = "datasets/Updated_Previous_Courses_Dataset.csv"

# Recommendation Logic
def recommend_courses(request):
    # Load datasets
    students_df = pd.read_csv(STUDENTS_DATASET)
    courses_df = pd.read_excel(COURSES_DATASET)
    previous_courses_df = pd.read_csv(PREVIOUS_COURSES)

    # Add random difficulty and duration (sample data enhancements)
    courses_df["Difficulty"] = [random.randint(1, 5) for _ in range(len(courses_df))]
    courses_df["Course_Duration"] = [random.randint(10, 60) for _ in range(len(courses_df))]

    # Label encoders and feature preparation
    grade_mapping = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    le_branch = LabelEncoder()
    le_goal = LabelEncoder()

    students_df["Branch_Encoded"] = le_branch.fit_transform(students_df["Branch"])
    students_df["Career_Goals_Encoded"] = le_goal.fit_transform(students_df["Career_Goals"])

    merged_df = previous_courses_df.merge(students_df, on="Student_ID").merge(courses_df, on="Course_ID")
    merged_df["Grade"] = merged_df["Grade"].map(grade_mapping).fillna(0)

    feature_columns = ["Branch_Encoded", "Career_Goals_Encoded", "Difficulty", "Course_Duration", "Grade"]
    feature_matrix = merged_df[feature_columns]

    # Normalize and KNN
    scaler = StandardScaler()
    feature_matrix_scaled = scaler.fit_transform(feature_matrix)

    knn = NearestNeighbors(n_neighbors=5, metric="cosine")
    knn.fit(feature_matrix_scaled)

    if request.method == "POST":
        student_name = request.POST.get("student_name")
        student = students_df[students_df["Name"].str.contains(student_name, case=False, na=False)]

        if student.empty:
            return render(request, "recommendations/recommend_courses.html", {"error": "Student not found"})

        student_id = student.iloc[0]["Student_ID"]
        student_courses = merged_df[merged_df["Student_ID"] == student_id]
        student_features = student_courses[feature_columns].values
        student_features_scaled = scaler.transform(student_features)

        distances, indices = knn.kneighbors(student_features_scaled, n_neighbors=5)
        recommended_courses = set()

        for idx in indices.flatten():
            course_id = merged_df.iloc[idx]["Course_ID"]
            recommended_courses.add(course_id)

        taken_courses = set(student_courses["Course_ID"])
        new_courses = [course_id for course_id in recommended_courses if course_id not in taken_courses]

        return render(request, "recommendations/recommend_courses.html", {"courses": new_courses})

    return render(request, "recommendations/recommend_courses.html")
