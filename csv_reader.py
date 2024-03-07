"""
This is what we use to read in info from a CSV and covert it
into Python objects, a list of tuples
"""

import pandas as pd
from student_record import StudentRecord


class CSVReader:
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name

    def get_file_name(self) -> str:
        return self.file_name

    def set_file_name(self, file_name: str) -> None:
        self.file_name = file_name

    def read_values(self) -> list[StudentRecord]:
        studentRecordList: list[StudentRecord] = []

        # Read data from CSV file
        dataframe = pd.read_csv(self.file_name)
        headers: list = dataframe.columns.values.tolist()

        # Convert data from dataframe to list of StudentRecord
        for i in range(len(dataframe)):
            studentRecord:StudentRecord = StudentRecord(*(dataframe.loc[i].to_list()))
            studentRecordList.append(studentRecord)

        return studentRecordList


if __name__ == "__main__":
    from rich import print

    csv_reader = CSVReader("student_data2.csv")
    student_records: list[StudentRecord] = csv_reader.read_values()

    print(student_records)
