import psycopg2
from common import *

# Define your user story
us = '''
* Complex, Operational US

   As a:  Discord data analytics
 I want:  To cater ads to users based on servers they are in
So That:  I can make the ads approach the users more efficiently based on which servers users are in
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
def track_peak_usage_time(conn):
    try:
        cur = conn.cursor()

        cols = 'user_id user_name ads_id ads_name brand'

        tmpl = f'''
            SELECT 
                u.user_id AS user_id,
                u.user_name AS user_name,
                a.ads_id AS ads_id,
                a.ads_name AS ads_name,
                a.brand AS brand
            FROM 
                Users u
            JOIN 
                Membership m ON u.user_id = m.user_id
            JOIN 
                Partnership p ON m.server_id = p.server_id
            JOIN 
                Ads a ON p.ads_id = a.ads_id
            ORDER BY 
                u.user_id, a.ads_id;
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
        track_peak_usage_time(conn)
    finally:
        conn.close()
