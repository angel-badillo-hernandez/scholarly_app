"""Provides a class for accessing and operating on a SQLite database.

Provides the class `ScholarlyDatabase` for accessing a SQLite database
and inserting records in the students table and award criteria table.

"""

import sqlite3
import json
from student_record import StudentRecord
from award_criteria_record import AwardCriteriaRecord
from student_data_reader import StudentDataReader
from pypika import Query, Table, Field, Schema, Column, Columns, Order


class ScholarlyDatabase:
    """Class to operate SQLite3 database.

    Class to allow easy manipulation and operation of a SQLite database with
    the tables `students` and `award_criteria`.
    """

    __students_table_name: str = "students"
    __award_criteria_table_name: str = "award_criteria"
    __students_columns: list[Column] = Columns(
        ("name", "TEXT"),
        ("student_ID", "TEXT PRIMARY KEY"),
        ("cum_gpa", "REAL"),
        ("major", "TEXT COLLATE NOCASE"),
        ("classification", "TEXT COLLATE NOCASE"),
        ("earned_credits", "INTEGER"),
        ("enrolled", "TEXT COLLATE NOCASE"),
        ("email", "TEXT"),
        ("gender", "TEXT COLLATE NOCASE"),
        ("in_state", "TEXT COLLATE NOCASE"),
    )
    __award_criteria_columns: list[Column] = Columns(
        ("name", "TEXT PRIMARY KEY COLLATE NOCASE"),
        ("criteria", "JSON"),
        ("limit", "INTEGER"),
    )

    def __init__(self, file_path: str) -> None:
        """Creates an instance of ScholarlyDatabase.

        Creates an instance of ScholarlyDatabase for accessing and
        performing queries on the SQLite3 database.

        Args:
            file_path (str): File path for the SQLite3 database.
        """
        self.file_path: str = file_path

    @classmethod
    def students_table_name(cls) -> str:
        """Returns the name of the `students` table.

        Returns the name of the `students` table.

        Returns:
            Name of the `students` table as a `str`.
        """
        return cls.__students_table_name

    @classmethod
    def award_criteria_table_name(cls) -> str:
        """Returns the name of the `award_criteria` table.

        Returns the name of the `award_criteria` table.

        Returns:
            Name of the `award_criteria` table as a `str`.
        """
        return cls.__award_criteria_table_name

    @classmethod
    def students_table_columns(cls) -> list[Column]:
        """Returns the columns for the `students` table.

        Returns the columns for the `students` table.

        Returns:
            Columns for the `students` table as `list[Column]`.

        """
        return cls.__students_columns

    @classmethod
    def award_criteria_columns(cls) -> list[Column]:
        """Returns the columns for the `award_criteria` table.

        Returns the columns for the `award_criteria` table.

        Returns:
            Columns for the `award_criteria` table as `list[Column]`.

        """
        return cls.__award_criteria_columns

    def insert_student(self, record: StudentRecord) -> None:
        """Inserts a student record into the `students` table.

        Inserts a `StudentRecord` into the `students` table.

        Args:
            record (StudentRecord): A student record.
        """
        query: Query = Query.into(self.__students_table_name).insert(*record.to_tuple())
        conn: sqlite3.Connection = sqlite3.connect(self.file_path)
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(str(query))
        conn.commit()
        conn.close()

    def insert_award_criteria(self, record: AwardCriteriaRecord) -> None:
        """Inserts award critiera into the `award_criteria` table.

        Inserts award criteria into the `award_criteria` table.

        Args:
            record (AwardRecord): An award record.
        """
        query: Query = Query.into(self.__award_criteria_table_name).insert(
            record.name, json.dumps(record.criteria), record.limit
        )
        conn: sqlite3.Connection = sqlite3.connect(self.file_path)
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(str(query))
        conn.commit()
        conn.close()

    def create_table(self, table_name: str, columns: list[Column]):
        """Creates a table in a SQLite database.

        Creates a table in a SQlite Database file.

        Args:
            table_name (str): Name of the table.
            columns (list[Column]): Columns for the table.
        """
        query: Query = Query.create_table(table_name).columns(*columns).if_not_exists()

        conn: sqlite3.Connection = sqlite3.connect(self.file_path)
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(str(query))
        conn.commit()
        conn.close()

    def drop_table(self, table_name: str):
        """Drops a table from the database.

        Drops a table from the SQLite3 database.

        Args:
            table_name (str): Name of the table.
        """
        query: Query = Query.drop_table(table_name).if_exists()
        conn: sqlite3.Connection = sqlite3.connect(self.file_path)
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(str(query))
        conn.commit()
        conn.close()

    def select_award_criteria(self, award_name: str) -> AwardCriteriaRecord | None:
        """Gets the award criteria for a given award.

        Returns the award criteria for a given scholarship based on the name.

        Args:
            award_name (str): Name of the scholarship or award.
        Returns:
            Returns AwardCriteriaRecord if found, else returns None.
        """
        query: Query = (
            Query.from_(self.__award_criteria_table_name)
            .select("*")
            .where(Field("name") == award_name)
        )

        conn: sqlite3.Connection = sqlite3.connect(self.file_path)
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(str(query))

        data = cursor.fetchone()
        record: AwardCriteriaRecord = None
        # If record does exist
        if data:
            name, criteria, limit = data
            record = AwardCriteriaRecord(name, json.loads(criteria), limit)

        conn.commit()
        conn.close()

        return record

    def select_students_by_criteria(
        self, record: AwardCriteriaRecord
    ) -> list[StudentRecord]:
        """Get student records by criteria.

        Returns students records matching criteria from the `students` table.
        Args:
            record (AwardCriteriaRecord): Scholarship criteria.
        Returns:
            A list of StudentRecord matching the criteria for the award.
        """
        # The starting base query, if criteria is empty, becomes select all
        query: Query = (
            Query.from_(self.__students_table_name)
            .select("*")
            .orderby("cum_gpa", Order.desc)
        )

        # Add where clauses if criteria is not empty
        if record.criteria:
            # Iterate over criterion in criteria dict
            for field, item in record.criteria.items():
                # If the value for field is a dict, the apply conditions to query
                if isinstance(item, dict):
                    for key, val in item.items():
                        # If criteria is $in, check if value of field is in val
                        if key == "$in":
                            query = query.where(Field(field).isin(val))
                        # If criteria is $gte, check if val >= field
                        elif key == "$gte":
                            query = query.where(Field(field) >= val)
                # If the value for field is not a dict, simply match for equality
                else:
                    query = query.where(Field(field) == item)
        # If limit is specified, and no 0, add limit
        if record.limit:
            query = query.limit(record.limit)

        conn: sqlite3.Connection = sqlite3.connect(self.file_path)
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(str(query))

        data = cursor.fetchall()
        conn.commit()
        conn.close()

        student_records: list[StudentRecord] = []
        for record in data:
            student_records.append(StudentRecord(*record))

        return student_records

    def select_all_students(self) -> list[StudentRecord]:
        """Gets all the student records.

        Returns all the student records from the `students` table.

        Returns:
            All of the student records as StudentRecords
        """
        query: Query = (
            Query.from_(self.__students_table_name)
            .select("*")
            .orderby("cum_gpa", order=Order.desc)
        )

        conn: sqlite3.Connection = sqlite3.connect(self.file_path)
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(str(query))

        data = cursor.fetchall()
        conn.commit()
        conn.close()

        student_records: list[StudentRecord] = []
        for record in data:
            student_records.append(StudentRecord(*record))

        return student_records

    def student_csv_to_table(self, file_path: str):
        """Gets student records from CSV and stores in the table.

        Reads in student records from a CSV file and stores them in
        the `students` table.

        Args:
            file_path (str): File path for the CSV file.
        """
        self.drop_table(self.__students_table_name)
        self.create_table(self.__students_table_name, self.__students_columns)

        reader: StudentDataReader = StudentDataReader(file_path)
        data: list[StudentRecord] = reader.read_values()

        # Insert student records into database
        for record in data:
            self.insert_student(record)

    def award_criteria_json_to_table(self, file_path: str):
        """Convienience function for populating table.

        Function to assist with populating award criteria table.

        Args:
            file_path (str): File path to JSON file.
        """
        with open(file_path, "r") as file:
            data: list = json.load(file)

            for record in data:
                self.insert_award_criteria(AwardCriteriaRecord(**record))

    def select_all_award_criteria(self) -> list[AwardCriteriaRecord]:
        """Returns all award criteria.

        Returns all award criteria in the table.

        Returns:
            A list of AwardCriteriaRecord.
        """
        query: Query = (
            Query.from_(self.__award_criteria_table_name)
            .select("*")
            .orderby("name", order=Order.asc)
        )

        conn: sqlite3.Connection = sqlite3.connect(self.file_path)
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(str(query))

        data: list = cursor.fetchall()
        conn.commit()
        conn.close()

        award_records: list[AwardCriteriaRecord] = []

        for name, criteria, limit in data:
            award_records.append(AwardCriteriaRecord(name, json.loads(criteria), limit))
        return award_records


# Example sqlite3 operations
if __name__ == "__main__":
    from rich import print

    db = ScholarlyDatabase("database/scholarly.sqlite")

    db.drop_table(ScholarlyDatabase.award_criteria_table_name())
    db.student_csv_to_table("example_data/student_data2.csv")
    db.create_table(
        ScholarlyDatabase.award_criteria_table_name(),
        ScholarlyDatabase.award_criteria_columns(),
    )

    db.award_criteria_json_to_table("scholarships.json")
    c = db.select_award_criteria("Tom C. White")
    print(c)
    stud = db.select_students_by_criteria(c)
    print(stud)
