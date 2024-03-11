"""Provides a class for award criteria.

Provides the class `AwardRecord` for storing award criteria and converting it
into other data structures for ease of use in the SQLite database.
"""


class AwardRecord:
    """Represents award criteria.
    Class for representing student information. Allows easy conversion
    to dict, tuple, list, and SQLite insertable record/row.
    """

    def __init__(self, name: str = "", criteria: dict[str] = {}) -> None:
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
        self.criteria: str = criteria

    def __iter__(self):
        yield "name", self.name
        yield "criteria", self.criteria

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

    x = AwardRecord("Scholarship", {"cum_gpa": {"$gte": 4.0}})

    print(f"SQLite record/row:  {x.to_tuple()}")
    print(f"Dictionary: {dict(x)}")
    print(f"Tuple: {tuple(x)}")
    print(f"String representation: {x}")
