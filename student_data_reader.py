"""
This is what we use to read in info from a CSV and covert it
into Python objects, a list of tuples
"""

import pandas as pd
from student_record import StudentRecord


class StudentDataReader:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path

    def get_file_path(self) -> str:
        return self.file_path

    def set_file_path(self, file_name: str) -> None:
        self.file_path = file_name

    def read_values(self) -> list[StudentRecord]:
        studentRecordList: list[StudentRecord] = []

        # Read data from CSV file
        dataframe:pd.DataFrame = pd.read_csv(self.file_path)
        # headers: list = dataframe.columns.values.tolist()

        # Convert data from dataframe to list of StudentRecord
        for i in range(len(dataframe)):
            studentRecord:StudentRecord = StudentRecord(*(dataframe.loc[i].to_list()))
            studentRecordList.append(studentRecord)

        return studentRecordList


if __name__ == "__main__":
    from rich import print

    csv_reader = StudentDataReader("student_data2.csv")
    student_records: list[StudentRecord] = csv_reader.read_values()

    print(student_records)
