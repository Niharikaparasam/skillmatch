# recommendations/recommendations_logic.py
import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors

# Load data (Note: you should handle file paths appropriately in a production setting)
students_df = pd.read_csv("Students_Dataset (1).csv")
courses_df = pd.read_csv("Updated_Courses_Dataset.xls")
previous_courses_df = pd.read_csv("Updated_Previous_Courses_Dataset.csv")

# Generate random difficulty and course duration
courses_df["Difficulty"] = [random.randint(1, 5) for _ in range(len(courses_df))]
courses_df["Course_Duration"] = [random.randint(10, 60) for _ in range(len(courses_df))]

# Grade mapping
grade_mapping = {
    'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0
}

# Feature matrix preparation
def prepare_feature_matrix(students_df, courses_df, previous_courses_df):
    le_branch = LabelEncoder()
    le_goal = LabelEncoder()
    
    students_df["Branch_Encoded"] = le_branch.fit_transform(students_df["Branch"])
    students_df["Career_Goals_Encoded"] = le_goal.fit_transform(students_df["Career_Goals"])
    
    # Merge previous courses with students and courses
    merged_df = previous_courses_df.merge(students_df, on="Student_ID").merge(courses_df, on="Course_ID")
    
    merged_df["Grade"] = merged_df["Grade"].map(grade_mapping)
    merged_df["Grade"] = merged_df["Grade"].fillna(0)
    
    # Features for the recommendation
    feature_columns = ["Branch_Encoded", "Career_Goals_Encoded", "Difficulty", "Course_Duration", "Grade"]
    feature_matrix = merged_df[feature_columns]
    
    return feature_matrix, merged_df, le_branch, le_goal

# Normalize data and apply KNN
def get_knn_recommendations(students_df, courses_df, previous_courses_df, student_name, n_recommendations=5):
    feature_matrix, merged_df, le_branch, le_goal = prepare_feature_matrix(students_df, courses_df, previous_courses_df)
    
    # Normalize
    scaler = StandardScaler()
    feature_matrix_scaled = scaler.fit_transform(feature_matrix)
    
    # KNN model
    knn = NearestNeighbors(n_neighbors=5, metric="cosine")
    knn.fit(feature_matrix_scaled)
    
    # Find the student
    student = students_df[students_df["Name"].str.contains(student_name, case=False, na=False)]
    
    if student.empty:
        print(f"No student found with the name '{student_name}'.")
        return
    
    student_id = student.iloc[0]["Student_ID"]
    student_courses = merged_df[merged_df["Student_ID"] == student_id]
    
    student_features = student_courses[["Branch_Encoded", "Career_Goals_Encoded", "Difficulty", "Course_Duration", "Grade"]].values
    student_features_scaled = scaler.transform(student_features)
    
    distances, indices = knn.kneighbors(student_features_scaled, n_neighbors=5)
    
    # Get recommended courses
    recommended_courses = set()
    for idx in indices.flatten():
        neighbor_courses = merged_df.iloc[idx]["Course_ID"]
        recommended_courses.add(neighbor_courses)
    
    taken_courses = set(student_courses["Course_ID"])
    recommended_courses = [course_id for course_id in recommended_courses if course_id not in taken_courses]
    
    if recommended_courses:
        print("\nRecommended Courses:")
        for course_id in recommended_courses[:n_recommendations]:
            course_info = courses_df[courses_df["Course_ID"] == course_id]
            if not course_info.empty:
                course_info = course_info.iloc[0]
                print(f"{course_info['Course_Name']} (Provider: {course_info['Provider']}) - Difficulty: {course_info['Difficulty']}")
    else:
        print("\nNo new course recommendations based on the nearest neighbors.")

