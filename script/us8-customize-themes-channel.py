import psycopg2

# Define your user story
us = '''
* Simple US

   As a:  Moderator
 I want:  To customize themes for my server like stickers, audio, etc.
So That:  I can bring a sense of community to the server
'''

print(us)

# Database connection setup
conn = psycopg2.connect(
    dbname="project",
    user="isdb",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Define the modify_server_theme function
create_modify_server_theme_function = """
DROP FUNCTION IF EXISTS modify_server_theme();

CREATE OR REPLACE FUNCTION modify_server_theme(p_server_id INT, p_new_theme TEXT)
RETURNS void
LANGUAGE plpgsql AS
$$
BEGIN
    -- Check if the server exists and the theme needs to be updated
    IF EXISTS (SELECT 1 FROM Servers WHERE server_id = p_server_id AND theme IS NOT NULL AND theme <> '') THEN
        UPDATE Servers
        SET theme = p_new_theme
        WHERE server_id = p_server_id;
        RAISE NOTICE 'Theme updated for server_id % to %', p_server_id, p_new_theme;
    ELSE
        RAISE NOTICE 'Server ID % not eligible for theme update or does not exist', p_server_id;
    END IF;
END
$$;
"""

# Execute the function and modify themes
try:
    # Create the modify_server_theme function
    cursor.execute(create_modify_server_theme_function)
    print("Function modify_server_theme created successfully.")

    # Call the function with specific inputs
    server_id = 106  
    new_theme = 'Fantasy World'  
    cursor.execute("SELECT modify_server_theme(%s, %s);", (server_id, new_theme))
    print(f"Theme updated for server_id={server_id} to '{new_theme}'.")

    cursor.execute("SELECT * FROM Servers;")
    rows = cursor.fetchall()
    print("Updated Servers table:")
    for row in rows:
        print(row)

    conn.commit()

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
