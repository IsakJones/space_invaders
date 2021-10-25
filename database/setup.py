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

# Create the players table, which includes name, high score, and the date of the game
cursor.execute("""
CREATE TABLE players(
    id SERIAL, 
    name VARCHAR(128) UNIQUE, 
    high_score INTEGER, 
    date DATE,
    PRIMARY KEY (id)
);
""")

# Crete the scores table with score, player name, datetime
cursor.execute("""
CREATE TABLE scores(
    id SERIAL,
    score INTEGER,
    player_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
);
""") 

# Commit changes 
connection.commit()

# Close cursor
cursor.close()

# Close connection
connection.close()