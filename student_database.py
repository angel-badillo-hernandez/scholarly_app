# Where we have the code for database operations
import sqlite3

# Example sqlite3 operations
if __name__ == "__main__":
    # connect / create db file
    conn:sqlite3.Connection = sqlite3.connect("students.sqlite")
    
    

    # close db connect
    conn.close()
