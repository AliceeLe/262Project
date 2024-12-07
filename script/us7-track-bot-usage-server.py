import psycopg2
from common import *

# Define your user story
us = '''
* Simple, Analytical US

   As a:  Moderator
 I want:  To track bot usage in my channel
So That:  I can identify which bots are most frequently used for the channel
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

# Define the function to view biggest servers
def track_bot_server(conn):
    try:
        cur = conn.cursor()

        cols = 'channel_id, bot_usage_count'

        tmpl = f'''
        SELECT 
            channel_id, COUNT(bots_id)
        FROM APIDevelopment
        GROUP BY channel_id
        ORDER BY channel_id;
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

if __name__ == "__main__":
    conn = connect_to_db()
    try:
        track_bot_server(conn)
    finally:
        conn.close()
