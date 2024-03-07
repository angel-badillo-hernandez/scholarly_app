# Student Record


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
        major:str = "",
        classification: str = "",
        earned_credits: int = 0,
        enrolled:str = "",
        email:str = "",
        gender: str = "",
        in_state:str =  "",
    ) -> None:
        self.name: str = name
        self.student_ID: str = student_ID
        self.cum_gpa: float = cum_gpa
        self.major:str = major
        self.classification: str = classification
        self.earned_credits: int = earned_credits
        self.enrolled:str = enrolled
        self.email:str = email
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

    def to_record(self) -> tuple:
        return tuple(dict(self).values())

    def __repr__(self) -> str:
        return f"{dict(self)}"


if __name__ == "__main__":
    from rich import print

    x = StudentRecord("M10", "Angel", 4.0, "Freshman", 120, "male", True)

    print(f"SQLite record/row:  {x.to_record()}")
    print(f"Dictionary: {dict(x)}")
    print(f"Tuple: {tuple(x)}")
    print(f"String representation: {x}")