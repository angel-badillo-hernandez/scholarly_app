"""Provides a class for storing student records.

Provides the class `StudentRecord` for storing student data and converting it
into other data structures for ease of use in SQLite database.
"""


class StudentRecord:
    """Represents student information.
    Class for representing student information. Allows easy conversion
    to dict, tuple, list, and SQLite insertable record/row.
    """

    def __init__(
        self,
        name: str = "",
        student_ID: str = "",
        cum_gpa: float = 0.0,
        major: str = "",
        classification: str = "",
        earned_credits: int = 0,
        enrolled: str = "",
        email: str = "",
        gender: str = "",
        in_state: str = "",
    ) -> None:
        """Creates a StudentRecord object.

        A class for storing and representing student data.

        Args:
            name (str): Name of the student.
            student_ID (str): Mustangs ID of the student.
            cum_gpa (float): Cumulative GPA of the student.
            major (str): Major of the student.
            classification (str): Classification of the student.
            earned_credits (str): Total earned credits of the student.
            enrolled (str): Enrollment status of the student ("Yes", "No").
            gender (str): Gender of the student.
            in_state (str): Whether or not the student is in state ("Yes", "No").
        """
        self.name: str = name
        self.student_ID: str = student_ID
        self.cum_gpa: float = cum_gpa
        self.major: str = major
        self.classification: str = classification
        self.earned_credits: int = earned_credits
        self.enrolled: str = enrolled
        self.email: str = email
        self.gender: str = gender
        self.in_state: bool = in_state

    def __iter__(self):
        yield "name", self.name
        yield "student_ID", self.student_ID
        yield "cum_gpa", self.cum_gpa
        yield "major", self.major
        yield "classification", self.classification
        yield "earned_credits", self.earned_credits
        yield "enrolled", self.enrolled
        yield "email", self.email
        yield "gender", self.gender
        yield "in_state", self.in_state

    def to_dict(self) -> dict[str]:
        return dict(self)

    def to_tuple(self) -> tuple:
        return tuple(dict(self).values())

    def to_list(self) -> list:
        return list(dict(self).values())

    def headers(self) -> list[str]:
        return list(dict(self).keys())

    def __repr__(self) -> str:
        return str(dict(self))


if __name__ == "__main__":
    from rich import print

    x = StudentRecord("M10", "Angel", 4.0, "Freshman", 120, "male", True)

    print(f"SQLite record/row:  {x.to_tuple()}")
    print(f"Dictionary: {dict(x)}")
    print(f"Tuple: {tuple(x)}")
    print(f"String representation: {x}")
