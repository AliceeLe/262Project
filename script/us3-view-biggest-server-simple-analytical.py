import psycopg2
from common import *

# Define your user story
us = '''
* US3: Simple, Analytical US

   As a:  Member
 I want:  To view the biggest server in my region 
So That:  I can discover active communities nearby 
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
def view_biggest_server(conn, region_input):
    try:
        cur = conn.cursor()

        cols = 'server_id tag num_of_member region'

        tmpl = f'''
        SELECT server_id, tag, num_of_member, region
        FROM Servers
        WHERE region = %s AND num_of_member = (SELECT MAX(num_of_member) 
                                               FROM Servers 
                                               WHERE region = %s)
        '''

        cmd = cur.mogrify(tmpl, (region_input, region_input))
        print_cmd(cmd)
        cur.execute(tmpl, (region_input, region_input))
        rows = cur.fetchall()
        show_table( rows, cols )

    except Exception as e:
        print("Error executing query:", e)
        raise

if __name__ == "__main__":
    conn = connect_to_db()
    try:
        view_biggest_server(conn, "China")
    finally:
        conn.close()
