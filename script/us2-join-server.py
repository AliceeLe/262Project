import psycopg2
from common import *

# Database connection setup
conn = psycopg2.connect(
    dbname="project",
    user="isdb",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Define your user story
us = '''
* Complex, Operational US

   As a:  Member
 I want:  To join a server 
So That:  I can interact with other users  
'''

print(us)

# Drop and Create the insert_membership Function
# Due to foreign key constraint, if user_id or server_id are non-existent, then 
# the function automatically reject
create_insert_membership_function = """
DROP FUNCTION IF EXISTS insert_membership(int, int, boolean);

CREATE FUNCTION insert_membership(p_user_id int, p_server_id int, p_is_muted boolean) 
RETURNS void
LANGUAGE plpgsql AS 
$$
BEGIN
    INSERT INTO Membership(user_id, server_id, is_muted)
    VALUES (p_user_id, p_server_id, p_is_muted);
END
$$;
"""

# Function to insert 
def insert_membership(user_id, server_id, is_muted, cursor):
    try:
        call_insert_membership = """
        SELECT insert_membership(%s, %s, %s);
        """
        cursor.execute(call_insert_membership, (user_id, server_id, is_muted))
        print(f"Membership inserted: user_id={user_id}, server_id={server_id}, is_muted={is_muted}")
    except Exception as e:
        print(f"Error inserting membership: {e}")

# Helper function to display tables
select_membership = """
SELECT * FROM Membership;
"""

select_server = """
SELECT * FROM Servers;
"""


# Create the fn_update_num_member Trigger Function
create_update_num_member_function = """
CREATE OR REPLACE FUNCTION fn_update_num_member()
RETURNS trigger
LANGUAGE plpgsql AS
$$
BEGIN
    UPDATE Servers
    SET num_of_member = COALESCE(num_of_member, 0) + 1
    WHERE server_id = NEW.server_id;
    RETURN NEW;
END
$$;
"""

# Create the Trigger
create_trigger = """
DROP TRIGGER IF EXISTS update_num_member ON Membership;

CREATE TRIGGER update_num_member
AFTER INSERT ON Membership
FOR EACH ROW
EXECUTE FUNCTION fn_update_num_member();
"""

try:
    cursor.execute(create_insert_membership_function)
    print("Function insert_membership created successfully.")

    # Change param of user_id and server_id here to test  
    insert_membership(205, 109, False, cursor)
    print("Membership inserted successfully.")
    
    cursor.execute(select_membership)
    membership_rows = cursor.fetchall()
    print("Membership table contents:")
    membership_cols = 'user_id server_id is_muted'
    show_table( membership_rows, membership_cols )

    cursor.execute(create_update_num_member_function)
    print("Function fn_update_num_member created successfully.")

    cursor.execute(create_trigger)
    print("Trigger update_num_member created successfully.")

    cursor.execute(select_server)
    server_rows = cursor.fetchall()
    print("Servers table contents:")
    server_cols = 'server_id tag num_of_member region theme'
    show_table( server_rows, server_cols )

    # Commit changes
    conn.commit()

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
