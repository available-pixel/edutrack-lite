from database.queries import add_student, get_all_students

# Add test student
add_student("John Doe", 16, "Male", "Grade 10")

# Fetch students
students = get_all_students()

for student in students:
    print(student)