from dotenv import load_dotenv
import os

load_dotenv()

URI = f"""
    postgres+psycopg2://
    {os.getenv("DBUSER")}:
    {os.getenv("DBPASS")}>@<
    {os.getenv("DBHOST")}:
    {os.getenv("DBPORT")}/
    {os.getenv("DBNAME")}
"""