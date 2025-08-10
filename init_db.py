from main import app, db, Student, Course, Instructor, Section, Enrollment
from datetime import datetime, date

def init_database():
    """Initialize the database with sample data"""
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Add sample students
        students = [
            Student(student_number=1001, name="Alice Johnson", dob=date(2000, 5, 15)),
            Student(student_number=1002, name="Bob Smith", dob=date(2001, 8, 22)),
            Student(student_number=1003, name="Carol Williams", dob=date(1999, 12, 10)),
            Student(student_number=1004, name="David Brown", dob=date(2000, 3, 8)),
            Student(student_number=1005, name="Eva Davis", dob=date(2001, 7, 25))
        ]
        
        # Add sample instructors
        instructors = [
            Instructor(instructor_name="Dr. Sarah Miller"),
            Instructor(instructor_name="Prof. John Wilson"),
            Instructor(instructor_name="Dr. Maria Garcia"),
            Instructor(instructor_name="Prof. Michael Chen")
        ]
        
        # Add sample courses
        courses = [
            Course(course_number=101, course_name="Introduction to Computer Science", credit_hours=3),
            Course(course_number=102, course_name="Data Structures", credit_hours=4, prerequisite=101),
            Course(course_number=201, course_name="Database Systems", credit_hours=3, prerequisite=102),
            Course(course_number=301, course_name="Software Engineering", credit_hours=4, prerequisite=201),
            Course(course_number=202, course_name="Web Development", credit_hours=3, prerequisite=101)
        ]
        
        # Add all records to the session
        for student in students:
            db.session.add(student)
        for instructor in instructors:
            db.session.add(instructor)
        for course in courses:
            db.session.add(course)
            
        # Commit the basic data first
        db.session.commit()
        
        # Add sample sections
        sections = [
            Section(course_number=101, instructor_name="Dr. Sarah Miller", semester="Fall", year=2024),
            Section(course_number=102, instructor_name="Prof. John Wilson", semester="Spring", year=2024),
            Section(course_number=201, instructor_name="Dr. Maria Garcia", semester="Fall", year=2024),
            Section(course_number=301, instructor_name="Prof. Michael Chen", semester="Spring", year=2024),
            Section(course_number=202, instructor_name="Dr. Sarah Miller", semester="Fall", year=2024)
        ]
        
        for section in sections:
            db.session.add(section)
        db.session.commit()
        
        # Add sample enrollments
        enrollments = [
            Enrollment(student_number=1001, section_identifier=1, grade="A"),
            Enrollment(student_number=1001, section_identifier=2, grade="B+"),
            Enrollment(student_number=1002, section_identifier=1, grade="B"),
            Enrollment(student_number=1002, section_identifier=5, grade="A-"),
            Enrollment(student_number=1003, section_identifier=2, grade="A"),
            Enrollment(student_number=1003, section_identifier=3, grade="B+"),
            Enrollment(student_number=1004, section_identifier=1, grade="B-"),
            Enrollment(student_number=1005, section_identifier=5, grade="A")
        ]
        
        for enrollment in enrollments:
            db.session.add(enrollment)
        db.session.commit()
        
        print("Database initialized with sample data!")
        print(f"Added {len(students)} students")
        print(f"Added {len(instructors)} instructors")
        print(f"Added {len(courses)} courses")
        print(f"Added {len(sections)} sections")
        print(f"Added {len(enrollments)} enrollments")

if __name__ == "__main__":
    init_database()
