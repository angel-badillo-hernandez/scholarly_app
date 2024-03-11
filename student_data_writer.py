"""
Info here.
"""

import pandas as pd
from student_record import StudentRecord


class StudentDataWriter:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path

    def get_file_path(self) -> str:
        return self.file_path

    def set_file_path(self, file_name: str) -> None:
        self.file_path = file_name

    def write_values(self, student_data:list[StudentRecord]) -> None:
        data:list[dict] = [student.to_dict() for student in student_data]

        dataframe:pd.DataFrame = pd.DataFrame.from_records(data)

        dataframe.to_csv(self.file_path, index=False)


if __name__ == "__main__":
    from rich import print

    csv_writer = StudentDataWriter("t.csv")

    csv_writer.write_values([StudentRecord("A", "A"), StudentRecord()])
