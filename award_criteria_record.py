"""Provides a class for award criteria.

Provides the class `AwardCriteriaRecord` for storing award criteria and converting it
into other data structures for ease of use in the SQLite database.
"""

from typing import Any


class AwardCriteriaRecord:
    """Represents award criteria.
    Class for representing student information. Allows easy conversion
    to dict, tuple, list, and SQLite insertable record/row.
    """

    def __init__(
        self,
        name: str,
        criteria: dict[str] = {},
        limit: int = 0,
        sort: list[tuple[str, Any]] = [["cum_gpa", -1]],
    ) -> None:
        """Creates a new instance of AwardCriteria Record.

        Args:
            name (str): The name of the scholarship.
            criteria (dict[str], optional): The query for retreiving appropriate student records. Defaults to {}.
            limit (int, optional): The maximum number of student records to retreive. Defaults to 0, which means no limit and retreives all matches.
            sort (list[tuple[str, Any]], optional): Specifies how to sort the records. Defaults to [["cum_gpa", -1]], which sorts results on descending cummulative GPA.
        """
        self.name: str = name
        self.criteria: dict[str] = criteria
        self.limit: int = limit
        self.sort: list[tuple[str, Any]] = sort

    def __iter__(self):
        """Allows for iterating over attributes.

        Allows for iterating over attributes and casting to other
        data structures.
        """
        yield "name", self.name
        yield "criteria", self.criteria
        yield "limit", self.limit
        yield "sort", self.sort

    def to_dict(self) -> dict[str]:
        """Returns dict representation of AwardCriteriaRecord.

        Returns a dict representation of the AwardCriteriaRecord object.

        Returns:
            A dict representation of the AwardCriteriaRecord object.
        """
        return dict(self)

    def to_tuple(self) -> tuple:
        """Returns tuple representation of AwardCriteriaRecord.

        Returns a tuple representation of the AwardCriteriaRecord object.

        Returns:
            A tuple representation of the AwardCriteriaRecord object.
        """
        return tuple(dict(self).values())

    def to_list(self) -> list:
        """Returns list representation of AwardCriteriaRecord.

        Returns a list representation of the AwardCriteriaRecord object.

        Returns:
            A list representation of the AwardCriteriaRecord object.
        """
        return list(dict(self).values())

    def headers(self) -> list[str]:
        """Returns the headers / keys.

        Returns the headers / keys pertaining to the attributes in
        the AwardCriteriaRecord object.

        Returns:
            A list of the headers / keys.
        """
        return list(dict(self).keys())

    def __repr__(self) -> str:
        """Returns a str representation.

        Returns a str representation of the AwardCriteriaRecord object.
        """
        return str(dict(self))


if __name__ == "__main__":
    from rich import print

    x = AwardCriteriaRecord("Scholarship", {"cum_gpa": {"$gte": 4.0}}, limit=4)

    print(f"Dictionary: {dict(x)}")
    print(f"Tuple: {tuple(x)}")
    print(f"String representation: {x}")

    x = [["d", 1]]

    for f, o in x:
        print(f, o)
