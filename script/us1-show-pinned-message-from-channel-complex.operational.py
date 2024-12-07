import psycopg2
from common import *

# Define your user story
us = '''
* Complex, Operational US

   As a:  Member
 I want:  To view all pinned messages in a specific channel 
So That:  I can view important messages 
'''

print(us)

# Define the database connection
def connect_to_db():
    try:
        # Connect to the `project` database
        conn = psycopg2.connect(
            dbname="project",
            user="isdb",         
            password="your_password",  
            host="localhost",    
            port="5432"          
        )
        conn.autocommit = True  
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        raise

# Define the function to list pinned messages
def list_pinned_messages(conn):
    try:
        cur = conn.cursor()

        cols = 'm.message_id, m.message_content, c.channel_id, u.user_id, u.user_name'

        tmpl = f'''
        SELECT {cols}
          FROM Messages as m
               JOIN Channel as c ON m.channel_id = c.channel_id
               JOIN Users as u ON m.user_id = u.user_id
         WHERE m.is_pinned = True 
        '''
        cmd = cur.mogrify(tmpl, ())
        print_cmd(cmd)
        cur.execute(cmd)
        rows = cur.fetchall()
        # pp(rows)
        show_table( rows, cols )

    except Exception as e:
        print("Error executing query:", e)
        raise

# Main program
if __name__ == "__main__":
    conn = connect_to_db()
    try:
        list_pinned_messages(conn)
    finally:
        conn.close()
