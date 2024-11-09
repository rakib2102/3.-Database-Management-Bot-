# import mysql.connector 
import sqlite3

from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the model and respond with SQL query
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])
        return response.text.strip()
    except Exception as e:
        logging.error("Error generating response: %s", e)
        return None

# # Connect to MySQL & execute query
# def execute_query(sql):
#     try:
#         # Connect to MySQL
#         with mysql.connector.connect(
#             host=os.getenv("MYSQL_HOST"),
#             user=os.getenv("MYSQL_USER"),
#             password=os.getenv("MYSQL_PASSWORD"),
#             database=os.getenv("MYSQL_DATABASE")
#         ) as connection:
#             with connection.cursor() as cursor:
#                 # Check SQL command
#                 if sql.strip().lower().startswith("select"):
#                     cursor.execute(sql)
#                     results = cursor.fetchall()
#                     columns = [desc[0] for desc in cursor.description]
#                     return {"type": "select", "data": results, "columns": columns}
#                 else:
#                     cursor.execute(sql)
#                     connection.commit()
#                     return {"type": "operation", "message": "Operation successful!"}
#     except mysql.connector.Error as e:
#         logging.error("Database error: %s", e)
#         return {"type": "error", "message": f"An error occurred: {e}"}

# Connect to SQLite & execute query
def execute_query(sql):
    try:
        # Connect to SQLite
        connection = sqlite3.connect('sample.db')
        cursor = connection.cursor()

        # Check the SQL command
        if sql.strip().lower().startswith("select"):
            cursor.execute(sql)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return {"type": "select", "data": results, "columns": columns}
        else:
            cursor.execute(sql)
            connection.commit()
            return {"type": "operation", "message": "Operation successful!"}
    except sqlite3.Error as e:
        logging.error("Database error: %s", e)
        return {"type": "error", "message": f"An error occurred: {e}"}
    finally:
        cursor.close()
        connection.close()

# Streamlit App
st.set_page_config(page_title="Text To SQL")
st.header("Text to SQL")

# User input
question = st.text_input("Input: ", key="input", placeholder="Type your SQL question here...")
submit = st.button("Submit")

# Prompt for the model
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the following tables and columns:

    1. **students**: (student_id, name, department_id, batch, section, course_id, marks)
    2. **courses**: (course_id, course_name, department_id)
    3. **departments**: (department_id, department_name)
    4. **enrollments**: (enrollment_id, student_id, course_id, semester)
    5. **payments**: (payment_id, student_id, amount, payment_date)

    Please note the following guidelines for generating SQL queries:
    - Do not include backticks (```) in the output.
    - Do not use single quotes (`'`) for string values or aliases.
    - Do not use double quotes (`"`) for aliases.
    - For aliases, use no delimiters (just the alias name) or backticks (``) only if necessary.
    - Do not use the word 'SQL' in your response.
    - Generate SQL queries without any additional delimiters.

    Here are some examples of how to phrase questions:
    \n1. Show me all the students.
    \n2. What are the courses available?
    \n3. List all students enrolled in the 'Artificial intelligence' course.
    \n4. Create a new course called 'Data Science' with 4 credits.
    \n5. Insert a new student with name 'John Doe' and department 'CSE'.
    \n6. Show me the payment details of Rakibul Islam.
    \n7. What is the department of Rakibul Islam?
    \n8. Show me the marks of Rakibul Islam.
    \n9. Update the department name from 'Computer Science' to 'CSE'.
    \n10. Delete the student named 'John Doe'.

    Ensure the generated queries are accurate and consider the relationships between tables where necessary.
    """
]

# Validate user input
def get_validated_input():
    user_input = question.strip()
    if not user_input:
        st.error("The input field is empty")
        return None
    return user_input

if submit:
    user_input = get_validated_input()
    if user_input:
        with st.spinner("Generating SQL query..."):
            response = get_gemini_response(user_input, prompt)
        
        if response:
            st.subheader("Generated SQL Query:")
            st.code(response)

            # Execute the query and retrieve data
            with st.spinner("Executing query..."):
                result = execute_query(response)
                
            # Handle the result based on types
            if result['type'] == "error":
                st.error(result['message'])
            elif result['type'] == "select":
                st.subheader("Query Results:")
                if result['data']:
                    st.write(result['columns'])
                    for row in result['data']:
                        st.write(row)
                else:
                    st.write("No results found.")
            elif result['type'] == "operation":
                st.success(result['message'])
