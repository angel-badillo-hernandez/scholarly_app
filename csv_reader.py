"""
This is what we use to read in info from a CSV and covert it
into Python objects, a list of tuples
"""
import csv
from student_record import StudentRecord

class CSVReader:
    def __init__(self, file_name:str) -> None:
        self.file_name:str = file_name
    
    def read_values(self)->list[StudentRecord]:
        with open(self.file_name, "r") as file:
            pass