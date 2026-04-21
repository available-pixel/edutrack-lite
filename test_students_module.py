from modules.students import create_student, list_students

# Add a student
result = create_student("Alice Smith", 15, "Female", "Grade 9")
print(result)

# List students
students = list_students()

for s in students:
    print(s)