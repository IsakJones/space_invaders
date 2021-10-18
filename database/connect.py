import psycopg2 as pg


# Open the connection with the db
connection = pg.connect(
    host="localhost",
    database="space_invaders_db",
    user="space_invaders",
    password="password98"
)

# Initialize the cursor, which allows to input queries
cursor = connection.cursor()
# Execute a command
cursor.execute("SELECT id, name FROM employees")
# Take in the output
rows = cursor.fetchall() # Outputs tuples

for r in rows:
    print(f"id {r[0]}, name {r[1]}")

# Close the cursor
cursor.close()

# Close the connection
connection.close()
