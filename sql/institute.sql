-- @block
CREATE DATABASE IF NOT EXISTS institute;

-- @block
USE institute;

-- @block
CREATE TABLE teachers(
	teacher_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50),
	subject VARCHAR(50),
	email VARCHAR(50),

	CHECK(subject IN('Math','Biology','Physics','Chemistry'))
);

-- @block
CREATE TABLE students(
	student_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50),
	email VARCHAR(50) UNIQUE,
	password TEXT,
	created_at DATE DEFAULT (CURRENT_DATE)
);

-- @block
CREATE TABLE classes(
	class_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50),
	teacher_id INT,
	schedule VARCHAR(50),
	capacity INT,
	description TEXT,

	FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id)
);

-- @block
CREATE TABLE enrollments(
	enroll_id INT PRIMARY KEY AUTO_INCREMENT,
	student_id INT,
	class_id INT,
	enrolled_at DATETIME DEFAULT NOW(),

	FOREIGN KEY(student_id) REFERENCES students(student_id),
	FOREIGN KEY(class_id) REFERENCES classes(class_id)
);

-- @block
INSERT INTO teachers(name,subject,email)
VALUES
('Carl Johnson','Math','cj11@gmail.com'),
('Big Smoke','Chemistry','smokeeee^-^@gmail.com'),
('Cesar Vinsmoke','Math','cscscshi@gmail.com'),
('Sweet Johnson','Biology','johnson_sweet@gmail.com');

-- @block
SELECT * FROM teachers;

-- @block
INSERT INTO classes (name,teacher_id,schedule,capacity,description)
VALUES
('Calculas',1,'5:30 p.m | 7 p.m',10,'A begginer to intermediate calculas course for Computer Sceince students'),
('Atoms',2,'10 a.m | 11:30 a.m',1,'Learn everything about atoms with Professor Big Smoke'),
('Statistics',1,'3 p.m | 5p.m',5,'Essentials for Engineering'),
('Ecosystem',4,'6 a.m | 8a.m',50,'How our world works broken donw into simple words');

-- @block
SELECT * FROM classes;

-- @block
SELECT * FROM students;

-- @block
-- Sample students (passwords are plain text here only as demo/seed data,
-- matching how the app currently stores them - min 8 characters)
INSERT INTO students(name,email,password)
VALUES
('John Doe','john.doe@example.com','password123'),
('Jane Smith','jane.smith@example.com','securepass1'),
('Alex Turner','alex.turner@example.com','mypassword1');

-- @block
-- Sample enrollments (assumes the students and classes above already exist)
INSERT INTO enrollments(student_id,class_id)
VALUES
(1,1),
(1,3),
(2,2);

-- @block
SELECT * FROM enrollments;
