# Student Record


class StudentRecord:
    def __init__(
        self,
        studentID: str = "",
        name: str = "",
        cum_gpa: float = 0.0,
        classification: str = "",
        credit_hrs: int = 0,
        gender: str = "",
        address: str = "",
    ) -> None:
        self.id: str = studentID
        self.name: str = name
        self.cum_gpa: float = cum_gpa
        self.classification: str = classification
        self.credit_hrs: int = credit_hrs
        self.gender: str = gender
        self.address: str = address

    def __iter__(self):
        yield "id", self.id,
        yield "name", self.name,
        yield "cum_gpa", self.cum_gpa
        yield "classification", self.classification,
        yield "credit_hrs", self.credit_hrs
        yield "gender", self.gender,
        yield "address", self.address,

    def to_dict(self):
        return dict(self)
    
    def to_record(self):
        return tuple(dict(self).values())
    
    def __repr__(self) -> str:
        return f"{StudentRecord.__name__}(studentID={self.name})"

if __name__ == "__main__":
    from rich import print
    x = StudentRecord("M10", "Angel", 4.0, "Freshman", 120, "male", "Texas")
    
    print(x.to_record())
    print(dict(x))
    print(tuple(x))
    print(x)

    