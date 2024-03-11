"""Provides a class for writing StudentRecords to a CSV file.

Provides the class StudentDataWriter for writing a list of StudentRecord
to a CSV file.
"""

import pandas as pd
from student_record import StudentRecord


class StudentDataWriter:
    """Class for writing student data to a CSV file.

    Class for writing student data to a CSV file.
    """

    def __init__(self, file_path: str) -> None:
        """Creates an instance of StudentDataWriter.

        Creates a new instance of StudentDataWriter.

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

    def write_values(self, student_data: list[StudentRecord]) -> None:
        """Writes student data to a CSV file.

        Writes a list of student records to a CSV file.

        Args:
            student_data (list[StudentRecord]): A list of student records.
        """
        data: list[dict] = [student.to_dict() for student in student_data]

        dataframe: pd.DataFrame = pd.DataFrame.from_records(data)

        dataframe.to_csv(self.file_path, index=False)


if __name__ == "__main__":
    from rich import print

    csv_writer = StudentDataWriter("t.csv")

    csv_writer.write_values([StudentRecord("A", "A"), StudentRecord()])
