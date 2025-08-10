# Student Management System

A comprehensive web-based Student Management System built with Flask and SQLAlchemy. This application allows you to manage students, courses, instructors, sections, and enrollments.

## Features

- **Student Management**: View all students and individual student details with enrollment information
- **Course Management**: Browse courses and view course details with prerequisites
- **Instructor Management**: Manage instructor information and view their assigned sections
- **Section Management**: Handle course sections with instructor assignments
- **Enrollment Tracking**: Track student enrollments with grades

## Live Demo

🚀 **[Visit the Live Application](https://your-app-name.onrender.com)** (Link will be updated after deployment)

## Screenshots

The application includes several views:
- Home page with navigation
- Students listing and detailed student information
- Courses catalog with prerequisites
- Instructor profiles with assigned sections
- Section details with enrollments

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLAlchemy ORM with SQLite (for deployment)
- **Frontend**: HTML templates with CSS styling
- **Deployment**: Ready for cloud platforms (Railway, Render, Heroku)

## Local Development Setup

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/student-management-system.git
cd student-management-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Database Structure

The system includes the following entities:
- **Students**: Student information with unique student numbers
- **Courses**: Course catalog with credit hours and prerequisites
- **Instructors**: Instructor profiles
- **Sections**: Course sections taught by instructors
- **Enrollments**: Student enrollments in sections with grades

## API Routes

- `/` - Home page
- `/students/all` - List all students
- `/students/<id>` - Student details
- `/courses/all` - List all courses
- `/courses/<id>` - Course details
- `/instructors/all` - List all instructors
- `/instructors/<id>` - Instructor details
- `/sections/all` - List all sections
- `/sections/<id>` - Section details
- `/test_db` - Database connection test

## Deployment

This application is configured for easy deployment to cloud platforms:

### Railway/Render Deployment
1. Fork this repository
2. Connect your GitHub account to Railway/Render
3. Deploy directly from the repository
4. The application will automatically use SQLite database

### Environment Variables
- `DATABASE_URL`: Optional database connection string
- `PORT`: Application port (automatically set by hosting platforms)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Rahul** - Database Systems Project

## Acknowledgments

- Built as part of a Database Systems course
- Thanks to the Flask and SQLAlchemy communities for excellent documentation
