"""
Script to reset the database by dropping all tables and recreating them.
This will delete all existing data!
"""
import os
import sqlite3

# Path to the database
db_path = 'instance/quiz.db'

if os.path.exists(db_path):
    print(f"Deleting database file: {db_path}")
    os.remove(db_path)
    print("Database deleted successfully!")
else:
    print(f"Database file not found: {db_path}")

print("\nNow restart the Flask server with: python app.py")
print("The database will be recreated with the correct schema.")

