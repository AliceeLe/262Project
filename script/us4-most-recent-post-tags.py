import psycopg2
from common import *

# Define your user story
us = '''
* Simple, Analytical US

   As a:  Member
 I want:  To view the most recent post with specific tags 
So That:  I can find posts relevant to the topic I’m looking for 
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
def view_recent_post_with_tag(conn, tag_input):
    try:
        cur = conn.cursor()

        cols = 'post_id, post_content, post_time, tag, title, user_id, channel_id'

        tmpl = f'''
        SELECT post_id,post_content,post_time,tag,title,user_id,channel_id
        FROM Posts
        WHERE tag = %s AND post_time = (SELECT MAX(post_time) 
                                               FROM Posts 
                                               WHERE tag = %s)
        '''

        cmd = cur.mogrify(tmpl, (tag_input, tag_input))
        print_cmd(cmd)
        cur.execute(tmpl, (tag_input, tag_input))
        rows = cur.fetchall()
        show_table( rows, cols )

    except Exception as e:
        print("Error executing query:", e)
        raise

if __name__ == "__main__":
    conn = connect_to_db()
    try:
        view_recent_post_with_tag(conn, "general")
    finally:
        conn.close()
