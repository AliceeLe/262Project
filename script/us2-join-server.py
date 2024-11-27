import psycopg2

# Database connection setup
conn = psycopg2.connect(
    dbname="project",
    user="isdb",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Drop and Create the insert_membership Function
# Due to foreign key constraint, if user_id or server_id are non-existent, then 
# the function automatically reject
create_insert_membership_function = """
DROP FUNCTION IF EXISTS insert_membership(int, int);

CREATE FUNCTION insert_membership(p_user_id int, p_server_id int) 
RETURNS void
LANGUAGE plpgsql AS 
$$
BEGIN
    INSERT INTO Membership(user_id, server_id)
    VALUES (p_user_id, p_server_id);
END
$$;
"""

# Function to insert 
def insert_membership(user_id, server_id, cursor):
    try:
        call_insert_membership = """
        SELECT insert_membership(%s, %s);
        """
        cursor.execute(call_insert_membership, (user_id, server_id))
        print(f"Membership inserted: user_id={user_id}, server_id={server_id}")
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
    insert_membership(210, 109, cursor)
    print("Membership inserted successfully.")
    
    cursor.execute(select_membership)
    membership_rows = cursor.fetchall()
    print("Membership table contents:")
    for row in membership_rows:
        print(row)

    cursor.execute(create_update_num_member_function)
    print("Function fn_update_num_member created successfully.")

    cursor.execute(create_trigger)
    print("Trigger update_num_member created successfully.")

    cursor.execute(select_server)
    server_rows = cursor.fetchall()
    print("Servers table contents:")
    for row in server_rows:
        print(row)

    # Commit changes
    conn.commit()

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
