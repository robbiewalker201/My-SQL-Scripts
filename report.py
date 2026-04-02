'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Intro to AI with SQL - Add Databases to your Intelligent Projects

                    Eli the Computer Guy

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Import ollama functions
from ollama import chat, ChatResponse
# import sqlite
import sqlite3

# Define LLM Injection
# This will work as the rules you will set for the LLM's outputs
injection = "Reply in under 10 words"

class db:
    '''
    Create db
    '''
    def create():
        # connect or create database
        conn = sqlite3.connect("report-db.db")
        # Create cursor for active session
        cursor = conn.cursor()
        # Execute creation of table
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS thread (
                                query,
                                response,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                       
                       );
                       """)
        # Save changes and close session
        conn.commit()
        conn.close()

    '''
    Insert to db (write)
    '''
    def insert(query, response):
        # connect again
        conn = sqlite3.connect("report-db.db")
        # Create cursor
        cursor = conn.cursor()
        # SQL Insert Query
        sql_insert = "INSERT into thread(query, response) values(?,?)"
        # execute insert
        cursor.execute(sql_insert, (query, response)) 
        # Save changes and close session
        conn.commit()
        conn.close()

    '''
    Select from db (read)
    '''
    def select():
        # connect
        conn = sqlite3.connect("report-db.db")
        # Create cursor
        cursor = conn.cursor()
        # SQL SELECT Query
        sql_select = "SELECT * FROM thread"
        # Execute Query
        cursor.execute(sql_select)
        # assign results from cursor
        query_result = cursor.fetchall()
        # Close connection
        # No need to save as no changes have been made
        conn.close()
        
        return query_result
    
'''
Create report from sql read query
'''
def report():
    response = db.select()
    with open("ai-report.html", 'a') as f:
        for line in response:
            f.write(f'<p>{line}<p>')

'''
LLM function
'''
def ai(query):
  response: ChatResponse = chat(model='gemma3:1b', messages=[
    {
      'role': 'user',
      'content': query,
    },
  ])

  return response.message.content

db.create()

while True:
    user_input = input("Please Enter your Prompt: \n")
    query = f'query: {user_input}, injection: {injection}'
    ollama_response = ai(query)
    db.insert(query, ollama_response)
    report()
    print(f"You ask {user_input}?")
    print(ollama_response)