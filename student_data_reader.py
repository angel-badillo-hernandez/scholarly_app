"""Provides a class for reading in StudentRecord from a CSV file.

Provides the class StudentDataReader for reading in student data from
a CSV file.
"""

import pandas as pd
from student_record import StudentRecord


class StudentDataReader:
    """Class for reading in student data from a CSV file.

    Class for reading in student data from a CSV file.
    """

    def __init__(self, file_path: str) -> None:
        """Creates an instance of StudentDataReader

        Creates a new instance of StudentDataReader.

        Args:
            file_path (str): File path to the CSV file.
        """
        self.file_path: str = file_path

    def get_file_path(self) -> str:
        """Returns the file path for the CSV file.

        Returns the file path for the CSV file.

        Returns:
            File path as str for the CSV file.
        """
        return self.file_path

    def set_file_path(self, file_name: str) -> None:
        """Sets the file path for the CSV file.

        Sets the file path for the CSV file.

        Args:
            file_path (str): File path to the CSV file.
        """
        self.file_path = file_name

    def read_values(self) -> list[StudentRecord]:
        """Returns data from CSV file.

        Returns the student data from the CSV file as
        a list of StudentRecord.

        Returns:
            `list[StudentRecord]', a list of student records.
        """
        studentRecordList: list[StudentRecord] = []

        # Read data from CSV file
        dataframe: pd.DataFrame = pd.read_csv(self.file_path)
        # headers: list = dataframe.columns.values.tolist()

        # Convert data from dataframe to list of StudentRecord
        for i in range(len(dataframe)):
            studentRecord: StudentRecord = StudentRecord(*(dataframe.loc[i].to_list()))
            studentRecordList.append(studentRecord)

        return studentRecordList


if __name__ == "__main__":
    from rich import print

    csv_reader = StudentDataReader("student_data2.csv")
    student_records: list[StudentRecord] = csv_reader.read_values()

    print(student_records)
