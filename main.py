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

@app.route('/test_nav')
def test_nav():
    """Test route to check navigation"""
    return '''<h1>Navigation Test Successful!</h1>
              <p>If you can see this page, the navigation is working.</p>
              <p><a href="/">← Back to Home</a></p>'''

@app.route('/init_db')
def init_database_route():
    """Initialize the database with comprehensive sample data"""
    try:
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Add comprehensive student data
        students = [
            Student(student_number=2001, name="Emily Rodriguez", dob=date(2000, 3, 12)),
            Student(student_number=2002, name="James Thompson", dob=date(1999, 9, 18)),
            Student(student_number=2003, name="Sarah Kim", dob=date(2001, 1, 25)),
            Student(student_number=2004, name="Michael O'Connor", dob=date(2000, 7, 8)),
            Student(student_number=2005, name="Ashley Martinez", dob=date(1999, 11, 14)),
            Student(student_number=2006, name="David Anderson", dob=date(2001, 5, 3)),
            Student(student_number=2007, name="Jessica Wong", dob=date(2000, 12, 22)),
            Student(student_number=2008, name="Christopher Lee", dob=date(1999, 4, 16)),
            Student(student_number=2009, name="Amanda Taylor", dob=date(2001, 8, 30)),
            Student(student_number=2010, name="Ryan Johnson", dob=date(2000, 6, 7)),
            Student(student_number=2011, name="Lauren Brown", dob=date(1999, 10, 12)),
            Student(student_number=2012, name="Kevin Chen", dob=date(2001, 2, 28)),
            Student(student_number=2013, name="Natalie Davis", dob=date(2000, 9, 5)),
            Student(student_number=2014, name="Brandon Wilson", dob=date(1999, 12, 1)),
            Student(student_number=2015, name="Victoria Garcia", dob=date(2001, 4, 19))
        ]
        
        # Add diverse instructors
        instructors = [
            Instructor(instructor_name="Dr. Sarah Miller"),
            Instructor(instructor_name="Prof. John Wilson"),
            Instructor(instructor_name="Dr. Maria Garcia"),
            Instructor(instructor_name="Prof. Michael Chen"),
            Instructor(instructor_name="Dr. Jennifer Adams"),
            Instructor(instructor_name="Prof. Robert Taylor"),
            Instructor(instructor_name="Dr. Lisa Thompson"),
            Instructor(instructor_name="Prof. David Martinez"),
            Instructor(instructor_name="Dr. Amy Johnson"),
            Instructor(instructor_name="Prof. Mark Anderson")
        ]
        
        # Add comprehensive course curriculum
        courses = [
            # Computer Science Core
            Course(course_number=101, course_name="Introduction to Computer Science", credit_hours=3),
            Course(course_number=102, course_name="Programming Fundamentals", credit_hours=4),
            Course(course_number=201, course_name="Data Structures and Algorithms", credit_hours=4, prerequisite=102),
            Course(course_number=202, course_name="Computer Systems Architecture", credit_hours=3, prerequisite=101),
            Course(course_number=301, course_name="Database Systems", credit_hours=3, prerequisite=201),
            Course(course_number=302, course_name="Software Engineering", credit_hours=4, prerequisite=201),
            Course(course_number=401, course_name="Advanced Algorithms", credit_hours=3, prerequisite=301),
            Course(course_number=402, course_name="Machine Learning", credit_hours=4, prerequisite=301),
            
            # Mathematics
            Course(course_number=111, course_name="Calculus I", credit_hours=4),
            Course(course_number=112, course_name="Calculus II", credit_hours=4, prerequisite=111),
            Course(course_number=211, course_name="Linear Algebra", credit_hours=3, prerequisite=111),
            Course(course_number=311, course_name="Statistics and Probability", credit_hours=3, prerequisite=112),
            
            # Specialized Courses
            Course(course_number=351, course_name="Web Development", credit_hours=3, prerequisite=102),
            Course(course_number=352, course_name="Mobile App Development", credit_hours=3, prerequisite=201),
            Course(course_number=451, course_name="Cybersecurity Fundamentals", credit_hours=3, prerequisite=302),
            Course(course_number=452, course_name="Cloud Computing", credit_hours=3, prerequisite=301)
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
        
        # Add comprehensive sections for Fall 2024 and Spring 2025
        sections = [
            # Fall 2024 sections
            Section(course_number=101, instructor_name="Dr. Sarah Miller", semester="Fall", year=2024),
            Section(course_number=102, instructor_name="Prof. John Wilson", semester="Fall", year=2024),
            Section(course_number=201, instructor_name="Dr. Maria Garcia", semester="Fall", year=2024),
            Section(course_number=202, instructor_name="Prof. Michael Chen", semester="Fall", year=2024),
            Section(course_number=301, instructor_name="Dr. Jennifer Adams", semester="Fall", year=2024),
            Section(course_number=302, instructor_name="Prof. Robert Taylor", semester="Fall", year=2024),
            Section(course_number=111, instructor_name="Dr. Lisa Thompson", semester="Fall", year=2024),
            Section(course_number=112, instructor_name="Prof. David Martinez", semester="Fall", year=2024),
            Section(course_number=351, instructor_name="Dr. Amy Johnson", semester="Fall", year=2024),
            Section(course_number=451, instructor_name="Prof. Mark Anderson", semester="Fall", year=2024),
            
            # Spring 2025 sections
            Section(course_number=101, instructor_name="Prof. John Wilson", semester="Spring", year=2025),
            Section(course_number=102, instructor_name="Dr. Sarah Miller", semester="Spring", year=2025),
            Section(course_number=201, instructor_name="Prof. Michael Chen", semester="Spring", year=2025),
            Section(course_number=211, instructor_name="Dr. Lisa Thompson", semester="Spring", year=2025),
            Section(course_number=311, instructor_name="Prof. David Martinez", semester="Spring", year=2025),
            Section(course_number=352, instructor_name="Dr. Amy Johnson", semester="Spring", year=2025),
            Section(course_number=401, instructor_name="Dr. Maria Garcia", semester="Spring", year=2025),
            Section(course_number=402, instructor_name="Dr. Jennifer Adams", semester="Spring", year=2025),
            Section(course_number=452, instructor_name="Prof. Mark Anderson", semester="Spring", year=2025)
        ]
        
        for section in sections:
            db.session.add(section)
        db.session.commit()
        
        # Add realistic enrollments with varied grades
        enrollments = [
            # Student 2001 - Emily Rodriguez (Strong student)
            Enrollment(student_number=2001, section_identifier=1, grade="A"),
            Enrollment(student_number=2001, section_identifier=2, grade="A-"),
            Enrollment(student_number=2001, section_identifier=7, grade="B+"),
            Enrollment(student_number=2001, section_identifier=9, grade="A"),
            
            # Student 2002 - James Thompson
            Enrollment(student_number=2002, section_identifier=1, grade="B+"),
            Enrollment(student_number=2002, section_identifier=3, grade="B"),
            Enrollment(student_number=2002, section_identifier=8, grade="B-"),
            Enrollment(student_number=2002, section_identifier=10, grade="B+"),
            
            # Student 2003 - Sarah Kim (Excellent student)
            Enrollment(student_number=2003, section_identifier=2, grade="A"),
            Enrollment(student_number=2003, section_identifier=4, grade="A"),
            Enrollment(student_number=2003, section_identifier=7, grade="A-"),
            Enrollment(student_number=2003, section_identifier=11, grade="A"),
            
            # Student 2004 - Michael O'Connor
            Enrollment(student_number=2004, section_identifier=1, grade="B"),
            Enrollment(student_number=2004, section_identifier=2, grade="B+"),
            Enrollment(student_number=2004, section_identifier=9, grade="A-"),
            
            # Student 2005 - Ashley Martinez
            Enrollment(student_number=2005, section_identifier=3, grade="B-"),
            Enrollment(student_number=2005, section_identifier=5, grade="C+"),
            Enrollment(student_number=2005, section_identifier=8, grade="B"),
            
            # Student 2006 - David Anderson (Advanced student)
            Enrollment(student_number=2006, section_identifier=5, grade="A"),
            Enrollment(student_number=2006, section_identifier=6, grade="A-"),
            Enrollment(student_number=2006, section_identifier=13, grade="B+"),
            Enrollment(student_number=2006, section_identifier=17, grade="A"),
            
            # Student 2007 - Jessica Wong
            Enrollment(student_number=2007, section_identifier=1, grade="A-"),
            Enrollment(student_number=2007, section_identifier=7, grade="B+"),
            Enrollment(student_number=2007, section_identifier=12, grade="A"),
            
            # Student 2008 - Christopher Lee
            Enrollment(student_number=2008, section_identifier=2, grade="B"),
            Enrollment(student_number=2008, section_identifier=4, grade="B-"),
            Enrollment(student_number=2008, section_identifier=14, grade="B+"),
            
            # Student 2009 - Amanda Taylor
            Enrollment(student_number=2009, section_identifier=3, grade="A-"),
            Enrollment(student_number=2009, section_identifier=9, grade="B+"),
            Enrollment(student_number=2009, section_identifier=16, grade="A"),
            
            # Student 2010 - Ryan Johnson
            Enrollment(student_number=2010, section_identifier=6, grade="B+"),
            Enrollment(student_number=2010, section_identifier=13, grade="B"),
            Enrollment(student_number=2010, section_identifier=18, grade="B+"),
            
            # Additional enrollments for more students
            Enrollment(student_number=2011, section_identifier=1, grade="B"),
            Enrollment(student_number=2011, section_identifier=11, grade="B-"),
            Enrollment(student_number=2012, section_identifier=2, grade="A"),
            Enrollment(student_number=2012, section_identifier=15, grade="A-"),
            Enrollment(student_number=2013, section_identifier=7, grade="B+"),
            Enrollment(student_number=2013, section_identifier=19, grade="A"),
            Enrollment(student_number=2014, section_identifier=4, grade="C+"),
            Enrollment(student_number=2014, section_identifier=8, grade="B-"),
            Enrollment(student_number=2015, section_identifier=5, grade="A-"),
            Enrollment(student_number=2015, section_identifier=17, grade="B+")
        ]
        
        for enrollment in enrollments:
            db.session.add(enrollment)
        db.session.commit()
        
        return f'''<h2>🎉 Database Successfully Initialized!</h2>
        <div style="background: #f0f8ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3>📊 Data Summary:</h3>
            <ul style="font-size: 16px; line-height: 1.6;">
                <li><strong>{len(students)} Students</strong> - Diverse student body with realistic names and birthdates</li>
                <li><strong>{len(instructors)} Instructors</strong> - Faculty across multiple departments</li>
                <li><strong>{len(courses)} Courses</strong> - Complete CS curriculum with prerequisites</li>
                <li><strong>{len(sections)} Sections</strong> - Fall 2024 & Spring 2025 offerings</li>
                <li><strong>{len(enrollments)} Enrollments</strong> - Realistic grade distributions</li>
            </ul>
        </div>
        <div style="margin: 20px 0;">
            <h3>🔗 Explore Your System:</h3>
            <p><a href="/students/all" style="background: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin: 5px;">View All Students</a></p>
            <p><a href="/courses/all" style="background: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin: 5px;">View All Courses</a></p>
            <p><a href="/instructors/all" style="background: #17a2b8; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin: 5px;">View All Instructors</a></p>
            <p><a href="/sections/all" style="background: #ffc107; color: black; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin: 5px;">View All Sections</a></p>
        </div>
        <p><a href="/" style="background: #6c757d; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">← Back to Home</a></p>'''
    except Exception as e:
        return f'<h2>❌ Error initializing database:</h2><p style="color: red; font-family: monospace;">{str(e)}</p><p><a href="/">Back to Home</a></p>'



# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

