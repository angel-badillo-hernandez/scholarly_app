# Where we have the code for database operations
# Modify this as needed
import sqlite3
from student_record import StudentRecord
from csv_reader import CSVReader
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

    def insert(self, record:StudentRecord)->None:

        query:Query = Query.into(self.table_name).insert(*record.to_record())
        conn:sqlite3.Connection = sqlite3.connect(self.file_name)
        cursor:sqlite3.Cursor = conn.cursor()

        cursor.execute(str(query))
        conn.commit()
        conn.close()

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

    def select(self, query:Query, key=None)->list[StudentRecord]:
        conn:sqlite3.Connection = sqlite3.connect(self.file_name)
        cursor:sqlite3.Cursor = conn.cursor()
        cursor.execute(str(query))

        data = cursor.fetchall()
        conn.commit()
        conn.close()

        student_records:list[StudentRecord] = []
        for record in data:
            student_records.append(StudentRecord(*record))


        return student_records


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

    db.create_table(db.table_name, db.columns)

    #s = StudentRecord("Angel", "M1", 4.0, "CS", "G", 100, "Y", "a", "m", "yes")

    #db.insert(s)

    t = Table("students")
    q:Query = Query.from_(db.table_name).select("*").where(t.student_id == 'M1')
    print(db.select(q))