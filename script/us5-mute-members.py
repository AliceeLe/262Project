import psycopg2
from common import *

# Define your user story
us = '''
* Complex, Operational US

   As a:  Moderator
 I want:  To mute members in specific channel 
So That:  I can maintain order on the server  
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

# Define the mute_user function
create_mute_user_function = """
DROP FUNCTION IF EXISTS mute_user();

CREATE OR REPLACE FUNCTION mute_user(p_moderator_id INT, p_member_id INT, p_server_id INT)
RETURNS TEXT
LANGUAGE plpgsql AS
$$
BEGIN
    -- Check if moderator and member are different
    IF p_moderator_id = p_member_id THEN
        RETURN 'Moderator cannot mute themselves.';
    END IF;

    -- Check if both users are in the server
    IF NOT EXISTS (
        SELECT 1
        FROM Membership
        WHERE user_id = p_moderator_id AND server_id = p_server_id
    ) THEN
        RETURN 'Moderator is not a member of the server.';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM Membership
        WHERE user_id = p_member_id AND server_id = p_server_id
    ) THEN
        RETURN 'Member is not a member of the server.';
    END IF;

    -- Check if moderator has the ability to mute
    IF NOT EXISTS (
        SELECT 1
        FROM Permission
        WHERE user_id = p_moderator_id AND server_id = p_server_id AND able_mute = TRUE
    ) THEN
        RETURN 'Moderator does not have mute permission.';
    END IF;

    -- Set the member's is_muted to true
    UPDATE Membership
    SET is_muted = TRUE
    WHERE user_id = p_member_id AND server_id = p_server_id;

    RETURN 'Member muted successfully.';
END
$$;
"""

try:
    # Create the mute_user function
    cursor.execute(create_mute_user_function)
    print("Function mute_user created successfully.")
    print(create_mute_user_function)

    # Call the function with specific inputs
    moderator_id = 205
    member_id = 202
    server_id = 104

    cursor.execute("SELECT mute_user(%s, %s, %s);", (moderator_id, member_id, server_id))
    result = cursor.fetchone()[0]
    print(result)

    # Query and display the updated Membership table
    cursor.execute("SELECT * FROM Membership WHERE server_id = %s;", (server_id,))
    rows = cursor.fetchall()
    print()
    print("Updated Membership table:")
    cols = 'server_id user_id is_muted'
    show_table( rows, cols )

    conn.commit()

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
