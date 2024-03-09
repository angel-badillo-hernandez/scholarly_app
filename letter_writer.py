from docx import Document


class LetterVariables:
    variables: list[str] = [
        "{STUDENT_NAME}",
        "{DATE}",
        "{AMOUNT}",
        "{SCHOLARSHIP_NAME}",
        "{ACADEMIC_YEAR}",
        "{HALF_AMOUNT}",
        "{ACADEMIC_YEAR_FALL}",
        "{ACADEMIC_YEAR_SPRING}",
        "{SENDER_NAME}",
        "{SENDER_EMAIL}",
        "{SENDER_TITLE}",
    ]

    def __init__(
        self,
        student_name: str,
        date: str,
        amount: str,
        scholarship_name: str,
        academic_year: str,
        sender_name: str,
        sender_email: str,
        sender_title: str,
    ) -> None:
        self.student_name: str = student_name
        self.date: str = date
        self.amount: str = amount
        self.scholarship_name: str = scholarship_name
        self.academic_year: str = academic_year
        self.sender_name: str = sender_name
        self.sender_email: str = sender_email
        self.sender_title: str = sender_title
        self.half_amount: str = str(float(self.amount) / 2)

        fall_sem, spring_sem = self.academic_year.split("-")
        self.academic_year_fall: str = fall_sem
        self.academic_year_spring: str = spring_sem

    def __iter__(self):
        yield "{STUDENT_NAME}", self.student_name
        yield "{DATE}", self.date
        yield "{AMOUNT}", self.amount
        yield "{SCHOLARSHIP_NAME}", self.scholarship_name
        yield "{ACADEMIC_YEAR}", self.academic_year
        yield "{SENDER_NAME}", self.sender_name
        yield "{SENDER_EMAIL}", self.sender_email
        yield "{SENDER_TITLE}", self.sender_title
        yield "{HALF_AMOUNT}", self.half_amount
        yield "{ACADEMIC_YEAR_FALL}", self.academic_year_fall
        yield "{ACADEMIC_YEAR_SPRING}", self.academic_year_spring

    def to_dict(self):
        return dict(self)

    def __repr__(self):
        return str(dict(self))

    def get_variables():
        return LetterVariables.variables


class LetterWriter:

    def __init__(
        self,
        template_file_path: str,
        output_file_path: str,
        variables_dict: dict[str, str],
    ) -> None:
        self.template_file_path: str = template_file_path
        self.output_file_path: str = output_file_path
        self.variables_dict: dict[str, str] = variables_dict

    def get_template_file_path(self) -> str:
        return self.template_file_path

    def set_template_file_path(self, file_path: str) -> None:
        self.template_file_path = file_path

    def get_output_file_path(self) -> str:
        return self.output_file_path

    def set_output_file_path(self, file_path: str) -> None:
        self.output_file_path = file_path

    def get_variables_dict(self) -> dict[str, str]:
        return self.variables_dict

    def set_variables_dict(self, vars_dict: dict[str, str]) -> None:
        self.variables_dict = vars_dict

    def writer_letter(self):
        document = Document(self.template_file_path)

        for key, value in self.variables_dict.items():
            for paragraph in document.paragraphs:
                if key in paragraph.text:
                    runs = paragraph.runs
                    for item in runs:
                        if key in item.text:
                            item.text = item.text.replace(key, value)

        document.save(self.output_file_path)


if __name__ == "__main__":
    vars = LetterVariables(
        "Angel Badillo",
        "March 8, 2024",
        "1000",
        "Hardworking Scholarship",
        "2023-2024",
        "Angel Badillo",
        "email@email.com",
        "Computer Science Master",
    )
    l = LetterWriter("template_letter.docx", "test.docx", vars.to_dict())
    l.writer_letter()
