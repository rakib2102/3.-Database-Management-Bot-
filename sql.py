# import mysql.connector
from dotenv import load_dotenv


import sqlite3
import os

load_dotenv()

# # Connect to the Mysql Database
# connection = mysql.connector.connect(
#     host=os.getenv("MYSQL_HOST"),
#     user=os.getenv("MYSQL_USER"),
#     password=os.getenv("MYSQL_PASSWORD"),
#     database=os.getenv("MYSQL_DATABASE")
# )

db_path = os.path.join(os.getcwd(), 'sample.db')
connection = sqlite3.connect(db_path)

# Cursor for executing queries
cursor = connection.cursor()

# Drop tables if they already exist
cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS courses")
cursor.execute("DROP TABLE IF EXISTS departments")
cursor.execute("DROP TABLE IF EXISTS enrollments")
cursor.execute("DROP TABLE IF EXISTS payments")

# # Create table departments
# departments_table = """
# CREATE TABLE departments (
#     department_id INT PRIMARY KEY,
#     department_name VARCHAR(50)
# );
# """

departments_table = """
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT
);
"""
cursor.execute(departments_table)

# # Create table courses
# courses_table = """
# CREATE TABLE courses (
#     course_id INT PRIMARY KEY,
#     course_name VARCHAR(50),
#     department_id INT,
#     FOREIGN KEY(department_id) REFERENCES departments(department_id)
# );
# """

courses_table = """
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT,
    department_id INTEGER,
    FOREIGN KEY(department_id) REFERENCES departments(department_id)
);
"""
cursor.execute(courses_table)

# # Create table students
# students_table = """
# CREATE TABLE students (
#     student_id INT PRIMARY KEY,
#     name VARCHAR(25), 
#     department_id INT,
#     batch INT,
#     section VARCHAR(25),
#     course_id INT,
#     marks INT,
#     FOREIGN KEY(department_id) REFERENCES departments(department_id),
#     FOREIGN KEY(course_id) REFERENCES courses(course_id)
# );
# """

students_table = """
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    name TEXT, 
    department_id INTEGER,
    batch INTEGER,
    section TEXT,
    course_id INTEGER,
    marks INTEGER,
    FOREIGN KEY(department_id) REFERENCES departments(department_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);
"""
cursor.execute(students_table)

# # Create table enrollments
# enrollments_table = """
# CREATE TABLE enrollments (
#     enrollment_id INT PRIMARY KEY,
#     student_id INT,
#     course_id INT,
#     enrollment_date DATE,
#     FOREIGN KEY(student_id) REFERENCES students(student_id),
#     FOREIGN KEY(course_id) REFERENCES courses(course_id)
# );
# """

enrollments_table = """
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date TEXT,
    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);
"""
cursor.execute(enrollments_table)

# # Create table payments
# payments_table = """
# CREATE TABLE payments (
#     payment_id INT PRIMARY KEY,
#     student_id INT,
#     amount DECIMAL(10, 2),
#     payment_date DATE,
#     FOREIGN KEY(student_id) REFERENCES students(student_id)
# );
# """

payments_table = """
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    amount DECIMAL(10, 2),
    payment_date TEXT,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
);
"""
cursor.execute(payments_table)


# data for departments
cursor.execute("INSERT INTO departments VALUES (1, 'Computer Science')")
cursor.execute("INSERT INTO departments VALUES (2, 'Electrical Engineering')")
cursor.execute("INSERT INTO departments VALUES (3, 'Mechanical Engineering')")

# data for courses
cursor.execute("INSERT INTO courses VALUES (1, 'Artificial Intelligence', 1)")
cursor.execute("INSERT INTO courses VALUES (2, 'Machine Learning', 1)")
cursor.execute("INSERT INTO courses VALUES (3, 'Power Systems', 2)")

# data for students
cursor.execute("INSERT INTO students VALUES (235, 'Alice Johnson', 1, 9, 'A', 1, 80)")
cursor.execute("INSERT INTO students VALUES (236, 'Bob Smith', 2, 9, 'A', 3, 88)")
cursor.execute("INSERT INTO students VALUES (237, 'Charlie Brown', 1, 9, 'A', 2, 72)")
cursor.execute("INSERT INTO students VALUES (238, 'Diana Prince', 2, 9, 'A', 3, 90)")
cursor.execute("INSERT INTO students VALUES (239, 'Rakibul Islam', 1, 9, 'A', 1, 85)")

# data for enrollments
cursor.execute("INSERT INTO enrollments VALUES (101, 235, 1, '2024-09-01')")
cursor.execute("INSERT INTO enrollments VALUES (102, 236, 3, '2024-09-02')")
cursor.execute("INSERT INTO enrollments VALUES (103, 237, 2, '2024-09-03')")
cursor.execute("INSERT INTO enrollments VALUES (104, 238, 3, '2024-09-04')")
cursor.execute("INSERT INTO enrollments VALUES (105, 239, 1, '2024-09-05')")

# data for payments
cursor.execute("INSERT INTO payments VALUES (201, 235, 1000.00, '2024-09-01')")
cursor.execute("INSERT INTO payments VALUES (202, 236, 1500.00, '2024-09-02')")
cursor.execute("INSERT INTO payments VALUES (203, 237, 1200.00, '2024-09-03')")

# Commit the changes
connection.commit()

# # Fetch and display the data from the table
# cursor.execute("SELECT * FROM students")
# rows = cursor.fetchall()

# print("Inserted Records in Students Table:")
# for row in rows:
#     print(row)

# Close the cursor and connection
cursor.close()
connection.close()