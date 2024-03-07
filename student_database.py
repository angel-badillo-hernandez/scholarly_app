# Where we have the code for database operations
# Modify this as needed
import sqlite3
from student_record import StudentRecord
from pypika import Query, Table, Field, Schema, Column, Columns  # use this if you want


class StudentDataBase:
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name
        self.table_name:str = "students"
        self.columns:list[Column] = Columns(
            ("name", "TEXT"),
            ("student_ID", "TEXT PRIMARY KEY"),
            ("cum_gpa", "REAL"),
            ("major", "TEXT"),
            ("classification", "TEXT"),
            ("earned_credits", "INTEGER"),
            ("enrolled", "TEXT"),
            ("email", "TEXT"),
            ("gender", "TEXT"),
            ("in_state", "TEXT"),
        )

        self.create_table("students", self.columns)

    def create_table(self, table_name: str, columns:list[Column]):
        """Creates a table in a SQLite database file.
        
        Creates a table in a SQlite Database file.
        
        """
        query:Query = Query.create_table(table_name).columns(*self.columns).if_not_exists()
        
        conn:sqlite3.Connection = sqlite3.connect(self.file_name)
        cursor:sqlite3.Cursor = conn.cursor()

        cursor.execute(str(query))
        conn.commit()
        conn.close()

    def drop_table(self, table_name:str):
        query:Query = Query.drop_table(table_name)
        conn:sqlite3.Connection = sqlite3.connect(self.file_name)
        cursor:sqlite3.Cursor = conn.cursor()

        cursor.execute(str(query))
        conn.commit()
        conn.close()

    def get_students(self):
        pass


# Example sqlite3 operations
if __name__ == "__main__":
    from rich import print
    # # connect / create db file
    # conn: sqlite3.Connection = sqlite3.connect("students.sqlite")
    # cursor: sqlite3.Cursor = conn.cursor()

    # cursor.execute("CREATE")

    # # close db connect
    # conn.close()
    db = StudentDataBase("file.sqlite")

    db.create_table("table1", db.columns)

    db.drop_table("table1")