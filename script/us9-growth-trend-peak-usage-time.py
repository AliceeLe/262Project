import psycopg2
from common import *

# Define your user story
us = '''
* Complex, Analytical US

   As a:  Discord data analytics
 I want:  To see the peak usage time for Discord
So That:  I can optimize features and introduce new user stories
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

        cols = 'usage_date usage_day usage_hour activity_count rank'

        tmpl = f'''
            WITH combined_usage AS (
                SELECT
                    EXTRACT(DOW from time) as usage_date,
                    TO_CHAR(time, 'Day') AS usage_day,
                    EXTRACT(HOUR from time) as usage_hour,
                    COUNT(*) AS total_messages
                FROM Messages
                GROUP BY usage_date, time, usage_hour

                UNION ALL

                SELECT
                    EXTRACT(DOW from post_time) as usage_date,
                    TO_CHAR(post_time, 'Day') AS usage_day,
                    EXTRACT(HOUR from post_time) as usage_hour,
                    COUNT(*) AS total_messages
                FROM Posts
                GROUP BY usage_date, post_time, usage_hour
            )

        SELECT
            usage_date,
            usage_day,
            usage_hour,
            SUM(total_messages) AS total_activity,
            DENSE_RANK() OVER (ORDER BY SUM(total_messages) DESC) AS rank
        FROM combined_usage
        GROUP BY usage_date, usage_day, usage_hour
        ORDER BY rank, usage_day, usage_hour;
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
