# https://developers.google.com/forms/api/quickstart/python
from google.oauth2.credentials import Credentials
from scholarly_google_auth import google_oauth
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from httplib2 import Http
from datetime import datetime


def create_outstanding_student_awards_form(
    credentials: Credentials,
    freshman_men: list[str],
    freshman_women: list[str],
    sophomore_men: list[str],
    sophomore_women: list[str],
    junior_men: list[str],
    junior_women: list[str],
    senior_men: list[str],
    senior_women: list[str],
    graduate_men: list[str],
    graduate_women: list[str],
) -> str:
    """Creates a Google Form for the Outstanding Student Awards.

    Args:
        credentials (Credentials): Google OAuth credentials.
        freshman_men (list[str]): List of fresh men candidates.
        freshman_women (list[str]): List of freshman women candidates.
        sophomore_men (list[str]): List of sophomore men candidates.
        sophomore_women (list[str]): List of sophomore women candidates.
        junior_men (list[str]): List of junior men candidates.
        junior_women (list[str]): List of junior women candidates.

        senior_men (list[str]): List of senior men candidates.
        senior_women (list[str]): List of senior women candidates.
        graduate_men (list[str]): List of graduate men candidates.
        graduate_women (list[str]): List of graduate women candidates.

    Returns:
        str: Link to the Google Form.
    """
    # # Create Gmail API client
    # service: Resource = build("forms", "v1", credentials=credentials)

    date: str = datetime.now().ctime()

    title: str = "Outstanding Student Awards"

    documentTitle: str = f"Outstanding Student Awards Form - {date}"

    description: str = (
        'Voting form for Outstanding Student Awards. Please select or enter a student of your choice in "Other" option in each category.'
    )

    # Create question for freshman man
    f_man_a: list[dict] = build_options(freshman_men, True)

    f_man_q: dict = build_question_body(
        "Outstanding Freshman Man",
        "Pick a candidate for Outstanding Freshman Man.",
        True,
        "RADIO",
        f_man_a,
        True,
        0,
    )

    # Create question for freshman woman
    f_woman_a: list[dict] = build_options(freshman_women, True)

    f_woman_q: dict = build_question_body(
        "Outstanding Freshman Woman",
        "Pick a candidate for Outstanding Freshman Woman.",
        True,
        "RADIO",
        f_woman_a,
        True,
        1,
    )

    # Create question for sophomore man
    s_man_a: list[dict] = build_options(sophomore_men, True)

    s_man_q: dict = build_question_body(
        "Outstanding Sophomore Man",
        "Pick a candidate for Outstanding Sophomore Man.",
        True,
        "RADIO",
        s_man_a,
        True,
        2,
    )

    # Create question for sophomore woman
    s_woman_a: list[dict] = build_options(sophomore_women, True)

    s_woman_q: dict = build_question_body(
        "Outstanding Sophmore Woman",
        "Pick a candidate for Outstanding Sophomore Woman.",
        True,
        "RADIO",
        s_woman_a,
        True,
        3,
    )

    # Create question for junior man
    j_man_a: list[dict] = build_options(junior_men, True)

    j_man_q: dict = build_question_body(
        "Outstanding Junior Man",
        "Pick a candidate for Outstanding Junior Man.",
        True,
        "RADIO",
        j_man_a,
        True,
        4,
    )

    # Create a question for junior woman
    j_woman_a: list[dict] = build_options(junior_women, True)

    j_woman_q: dict = build_question_body(
        "Outstanding Junior Woman",
        "Pick a candidate for Outstanding Junior Woman.",
        True,
        "RADIO",
        j_woman_a,
        True,
        5,
    )

    # Create a question for senior man
    sr_man_a: list[dict] = build_options(senior_men, True)

    sr_man_q: dict = build_question_body(
        "Outstanding Senior Man",
        "Pick a candidate for Outstanding Senior Man.",
        True,
        "RADIO",
        sr_man_a,
        True,
        6,
    )

    # Create a question for senior woman
    sr_woman_a: list[dict] = build_options(senior_women, True)

    sr_woman_q: dict = build_question_body(
        "Outstanding Senior Woman",
        "Pick a candidate for Outstanding Senior Woman",
        True,
        "RADIO",
        sr_woman_a,
        True,
        7,
    )

    # Create a question for graduate man
    g_man_a: list[dict] = build_options(graduate_men, True)

    g_man_q: dict = build_question_body(
        "Outstanding Graduate Man",
        "Pick a candidate for Outstanding Graduate Man",
        True,
        "RADIO",
        g_man_a,
        True,
        8,
    )

    # Create a question for graduate woman
    g_woman_a: list[dict] = build_options(graduate_women, True)

    g_woman_q: dict = build_question_body(
        "Outstanding Graduate Woman",
        "Pick a candidate for Outstanding Graduate Woman.",
        True,
        "RADIO",
        g_woman_a,
        True,
        9,
    )

    # Build list of questions
    questions: list[dict] = [
        f_man_q,
        f_woman_q,
        s_man_q,
        s_woman_q,
        j_man_q,
        j_woman_q,
        sr_man_q,
        sr_woman_q,
        g_man_q,
        g_woman_q,
    ]

    form_url: str = create_google_form(
        credentials=credentials,
        title=title,
        documentTitle=documentTitle,
        description=description,
        questions=questions,
    )

    return form_url


def create_google_form(
    credentials: Credentials,
    title: str,
    documentTitle: str,
    description: str,
    questions: list[dict],
) -> str:
    """Creates a basic Google Form with the specified parameters.

    Args:
        credentials (Credentials): Google OAuth credentials.
        title (str): Title of the form.
        documentTitle (str): Document title of the form.
        description (str): Description of the form.
        questions (list[dict]): List of questions.

    Returns:
        str: URL to the create Google Form.
    """
    # Create Gmail API client
    service: Resource = build("forms", "v1", credentials=credentials)

    # Request body for creating form
    form: dict = {
        "info": {
            "title": title,
            "documentTitle": documentTitle,
        }
    }

    # Request body for updating form (and adding questions)
    update_form_requests: dict[str, list] = {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {"description": description},
                    "updateMask": "description",
                },
            },
            *questions,
        ]
    }

    # Create form
    create_form_result = service.forms().create(body=form).execute()

    # Add questions
    question_setting = (
        service.forms()
        .batchUpdate(formId=create_form_result["formId"], body=update_form_requests)
        .execute()
    )

    # Get reponse body
    get_result = service.forms().get(formId=create_form_result["formId"]).execute()

    # Return form URI
    return get_result["responderUri"]


def build_question_body(
    title: str,
    description: str,
    required: bool,
    type: str,
    options: list[dict],
    shuffle: bool,
    index: int,
) -> dict:
    """Builds the portion of the create body required for creating a question.

    Args:
        title (str): Title of the question.
        description (str): Description of the question.
        required (bool): Whether or not the question is required to be answered.
        type (str): Type of question, e.g, "RADIO".
        options (list[dict]): List of options or "answers".
        shuffle (bool): Whether or not to shuffle the options.
        index (int): The index of where to insert the question in the form.

    Returns:
        dict: The portion of the request body for creating a question.
    """

    question_body: dict = {
        "createItem": {
            "item": {
                "title": title,
                "description": description,
                "questionItem": {
                    "question": {
                        "required": required,
                        "choiceQuestion": {
                            "type": type,
                            "options": options,
                            "shuffle": shuffle,
                        },
                    }
                },
            },
            "location": {"index": index},
        }
    }

    return question_body


def build_options(values: list[str], isOther: bool) -> list[dict]:
    """Builds the list of options that goes with the request body for creating a question.

    Args:
        values (list[str]): List of answers or selectable values.
        isOther (bool): Whether or not "Other" can be selected.

    Returns:
        list[dict]: List of options for a question.
    """
    options: list[dict] = [{"value": value} for value in values]

    if isOther:
        options.append({"isOther": True})

    return options


if __name__ == "__main__":
    from rich import print

    creds = google_oauth()

    names: list[str] = ["Student 1", "Student 2", "Student 3"]

    form_url: str = create_outstanding_student_awards_form(
        creds, names, names, names, names, names, names, names, names, names, names
    )

    print(form_url)
