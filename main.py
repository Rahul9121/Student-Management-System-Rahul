from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__, template_folder='templates')

# Use environment variable for database URL, fallback to SQLite for cloud deployment
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'
    student_number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, default=datetime.utcnow)

class Course(db.Model):
    __tablename__ = 'courses'
    course_number = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    credit_hours = db.Column(db.Integer)
    prerequisite = db.Column(db.Integer, db.ForeignKey('courses.course_number'))

class Instructor(db.Model):
    __tablename__ = 'instructors'
    instructor_name = db.Column(db.String(255), primary_key=True)

class Section(db.Model):
    __tablename__ = 'sections'
    section_identifier = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_number = db.Column(db.Integer, db.ForeignKey('courses.course_number'))
    instructor_name = db.Column(db.String(255), db.ForeignKey('instructors.instructor_name'))
    semester = db.Column(db.String(50))
    year = db.Column(db.Integer)
    enrollments = db.relationship('Enrollment', backref='related_section')
    course = db.relationship('Course', backref='sections')

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_number = db.Column(db.Integer, db.ForeignKey('students.student_number'))
    section_identifier = db.Column(db.Integer, db.ForeignKey('sections.section_identifier'))
    grade = db.Column(db.String(5))
    section = db.relationship('Section', back_populates='enrollments', overlaps="related_section")

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students/all')
def students_all():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/students/<int:id>')
def student_detail(id):
    student = Student.query.get(id)
    enrollments = Enrollment.query.join(Section, Enrollment.section_identifier == Section.section_identifier).join(Course, Section.course_number == Course.course_number).join(
        Instructor, Section.instructor_name == Instructor.instructor_name).filter(Enrollment.student_number == id).all()
    return render_template('student_detail.html', student=student, enrollments=enrollments)


@app.route('/instructors/<string:id>')
def instructor_detail(id):
    instructor = Instructor.query.get(id)
    sections = Section.query.join(Course).filter_by(instructor_name=id).all()
    return render_template('instructor_detail.html', instructor=instructor, sections=sections)


@app.route('/courses/all')
def courses_all():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get(course_id)
    prerequisites = Course.query.filter_by(prerequisite=course_id).all()
    return render_template('course_detail.html', course=course, prerequisites=prerequisites)


@app.route('/instructors/all')
def instructors_all():
    instructors = Instructor.query.all()
    return render_template('instructors.html', instructors=instructors)


@app.route('/sections/all')
def sections_all():
    sections = Section.query.all()
    return render_template('sections.html', sections=sections)


@app.route('/sections/<int:section_id>')
def section_detail(section_id):
    section = Section.query.get(section_id)
    return render_template('section_detail.html', section=section)


@app.route('/test_db')
def test_db():
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        return 'Database is connected'
    except:
        return 'Something went wrong'

@app.route('/init_db')
def init_database_route():
    """Initialize the database with sample data"""
    try:
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
        
        return f'Database initialized successfully!<br>Added {len(students)} students, {len(instructors)} instructors, {len(courses)} courses, {len(sections)} sections, and {len(enrollments)} enrollments.<br><br><a href="/">Go back to home</a>'
    except Exception as e:
        return f'Error initializing database: {str(e)}'



# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

