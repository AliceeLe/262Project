import psycopg2
from common import *

# Define your user story
us = '''
* US6: Simple, Operational US

   As a:  Moderator
 I want:  To retrieve message counts per user in a specific channel 
So That:  I can identify the most active contributors 
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

# Define the function to retrieve message count
def retrieve_message_count(conn, channel_id_input):
    try:
        cur = conn.cursor()

        cols = 'message_id, message_content, user_id, channel_id, post_count'

        tmpl = f'''
        SELECT 
            message_id, 
            message_content, 
            user_id, 
            channel_id,
            COUNT(message_id) OVER (PARTITION BY user_id, channel_id) AS post_count
        FROM Messages
        WHERE channel_id = %s;
        '''

        cmd = cur.mogrify(tmpl, (channel_id_input,))
        print_cmd(cmd)
        cur.execute(tmpl, (channel_id_input,))
        rows = cur.fetchall()

        # Display the results
        show_table(rows, cols)

    except Exception as e:
        print("Error executing query:", e)
        raise

if __name__ == "__main__":
    conn = connect_to_db()
    try:
        retrieve_message_count(conn, 3)
    finally:
        conn.close()