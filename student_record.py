# Student Record


class StudentRecord:
    """Represents student information.
    Class for representing student information. Allows easy conversion
    to dict, tuple, list, and SQLite insertable record/row.
    """

    def __init__(
        self,
        studentID: str = "",
        name: str = "",
        cum_gpa: float = 0.0,
        classification: str = "",
        credit_hrs: int = 0,
        gender: str = "",
        in_state: bool =  False,
    ) -> None:
        self.id: str = studentID
        self.name: str = name
        self.cum_gpa: float = cum_gpa
        self.classification: str = classification
        self.credit_hrs: int = credit_hrs
        self.gender: str = gender
        self.in_state: bool = in_state

    def __iter__(self):
        yield "id", self.id,
        yield "name", self.name,
        yield "cum_gpa", self.cum_gpa
        yield "classification", self.classification,
        yield "credit_hrs", self.credit_hrs
        yield "gender", self.gender,
        yield "in_state", self.in_state,

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