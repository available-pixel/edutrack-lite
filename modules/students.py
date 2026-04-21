from database.queries import add_student, get_all_students, student_exists


def create_student(name, age, gender, class_name):
    """
    Business logic for creating a student
    """

    # Normalize inputs
    name = name.strip().title() if name else ""
    class_name = class_name.strip() if class_name else ""

    # Validation
    if not name:
        return "Name is required"

    if not class_name:
        return "Class is required"

    if age is None or age < 3 or age > 25:
        return "Age must be between 3 and 25"

    if gender not in ["Male", "Female", "Other"]:
        return "Invalid gender"

    # Duplicate check (case-insensitive safer version)
    if student_exists(name):
        return f"{name} already exists"

    # Save
    add_student(name, age, gender, class_name)

    return f"{name} added successfully"

def list_students():
    """
    Return students in a clean format
    """
    students = get_all_students()

    formatted_students = []

    for s in students:
        student_dict = {
            "id": s[0],
            "name": s[1],
            "age": s[2],
            "gender": s[3],
            "class": s[4],
            "created_at": s[5]
        }
        formatted_students.append(student_dict)

    return formatted_students