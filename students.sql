CREATE TABLE Students (
    student_number INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE
);

CREATE TABLE Courses (
    course_number INT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    credit_hours INT,
    prerequisite INT,
    FOREIGN KEY (prerequisite) REFERENCES Courses(course_number)
);

CREATE TABLE Instructors (
    instructor_name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Sections (
    section_identifier INT PRIMARY KEY AUTO_INCREMENT,
    course_number INT,
    instructor_name VARCHAR(255),
    semester VARCHAR(50),
    year INT,
    FOREIGN KEY (course_number) REFERENCES Courses(course_number),
    FOREIGN KEY (instructor_name) REFERENCES Instructors(instructor_name)
);

CREATE TABLE Enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_number INT,
    section_identifier INT,
    grade VARCHAR(5),
    FOREIGN KEY (student_number) REFERENCES Students(student_number),
    FOREIGN KEY (section_identifier) REFERENCES Sections(section_identifier)
);





-- Insert data into Students table
INSERT INTO Students (student_number, name, dob) VALUES
(101, 'Alice Johnson', '1999-06-15'),
(102, 'Bob Smith', '2000-03-20'),
(103, 'Charlie Brown', '2001-11-25');

-- Insert data into Courses table
INSERT INTO Courses (course_number, course_name, credit_hours, prerequisite) VALUES
(1, 'Introduction to Programming', 3, NULL),
(2, 'Advanced Programming', 4, 1),
(3, 'Data Structures', 4, 2);

-- Insert data into Instructors table
INSERT INTO Instructors (instructor_name) VALUES
('Dr. John Doe'),
('Prof. Jane White'),
('Dr. Emily Green');

-- Insert data into Sections table
INSERT INTO Sections (course_number, instructor_name, semester, year) VALUES
(1, 'Dr. John Doe', 'Fall', 2023),
(2, 'Prof. Jane White', 'Spring', 2023),
(3, 'Dr. Emily Green', 'Summer', 2023);


-- Insert data into Enrollments table
INSERT INTO Enrollments (student_number, section_identifier, grade) VALUES
(101, 1, 'A'),
(101, 2, 'B'),
(102, 1, 'A'),
(102, 3, 'B'),
(103, 2, 'A');
