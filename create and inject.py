'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Intro to AI with SQL - Add Databases to your Intelligent Projects

                    Eli the Computer Guy

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Import ollama functions for LLM
from ollama import chat, ChatResponse
# Import sqlite for RDB
import sqlite3
# Import requests for APIs
# import requests

# Define preset injection for prompts
injection = 'Keep your response under 20 words'

'''''''''''''''''''''''''''''''''
    Lesson 1 - SQL Logging
'''''''''''''''''''''''''''''''''

class db:

    '''                   
    Function to create db
    '''                   
    def create():
        # connect to sqlite and create db
        # conn represents an active session with the database
        conn = sqlite3.connect("my-first-db.db")
        # Create cursor
        cursor = conn.cursor()
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS thread (
                                query,
                                response,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       );
                       """)
        # Save your changes to the database using .commit()
        # Writes the data from temp memory to disk space
        # SQLite does not auto commit in Python
        conn.commit()
        # Close the database
        conn.close()

    '''
    Function to insert to db
    '''
    def insert(query, response):
        # Connect to database - Create active session
        conn = sqlite3.connect("my-first-db.db")
        # Create cursor to interact with db
        cursor = conn.cursor()
        # Create SQL INSERT command
        # Insert user prompt and ollama response
        # Use ? as a placemolder that MUST be replaced with a value at the time of execution
        sql = "INSERT INTO thread(query, response) values(?,?)"
        # Execute query
        cursor.execute(sql,(query,response))
        # Commit changes
        conn.commit()
        # Close session
        conn.close()

'''
Function to generate LLM response
'''
def ai(query):

    # Create repsonse object for LLM output and annoted with 
    # suggested class
    response: ChatResponse = chat(model='gemma3:1b', messages=[
        {
            'role': 'user',
            'content': query,
        },
    ])

    # Return ollama response formatted
    return response.message.content

# Run database creation function
# Assign to object dtbse
dtbse = db.create()
# Print object
print(dtbse)

while True:
    user_input = input("Please Enter Prompt: \n")
    query = f'prompt: {user_input}, injection: {injection}'
    ollama_response = ai(query)
    db.insert(query, ollama_response)
    print(ollama_response)