import psycopg2
from common import *

us = '''
* Complex, Operational US

   As a:  Moderator
 I want:  To customize themes for my server like stickers, audio, etc.
So That:  I can bring a sense of community to the server
'''
print(us)

conn = psycopg2.connect(
    dbname="project",
    user="isdb",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

create_modify_server_theme_function = """
DROP FUNCTION IF EXISTS modify_server_theme();

CREATE OR REPLACE FUNCTION modify_server_theme(p_user_id INT, p_server_id INT, p_new_theme TEXT)
RETURNS void
LANGUAGE plpgsql AS
$$
BEGIN
    -- Check if the user has permission to customize the server
    IF EXISTS (
        SELECT 1
        FROM Permission
        WHERE user_id = p_user_id
          AND server_id = p_server_id
          AND able_customize = TRUE
    ) THEN
        UPDATE Servers
        SET theme = p_new_theme
        WHERE server_id = p_server_id;
    END IF;
END
$$;
"""

try:
    cursor.execute(create_modify_server_theme_function)
    print("Function modify_server_theme created successfully.")
    print(create_modify_server_theme_function)

    user_id = 205  
    server_id = 104  
    new_theme = 'Elegant Design'  
    cursor.execute("SELECT modify_server_theme(%s, %s, %s);", (user_id, server_id, new_theme))
    print(f"Attempted to update theme for server_id={server_id} by user_id={user_id} to '{new_theme}'.")

    cursor.execute("SELECT * FROM Servers;")
    rows = cursor.fetchall()
    print("Updated Servers table:")
    cols = 'server_id tag num_of_member region theme'
    show_table( rows, cols )

    conn.commit()

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
