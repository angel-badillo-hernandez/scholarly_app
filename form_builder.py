# https://developers.google.com/forms/api/quickstart/python
from google.oauth2.credentials import Credentials
from scholarly_google_auth import google_oauth
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from httplib2 import Http
from datetime import datetime


def create_form(
    credentials: Credentials,
    freshman_men: list[str],
    freshman_women: list[str],
    sophomore_men: list[str],
    sophomore_women: list[str],
    junior_men: list[str],
    junior_women: list[str],
    senior_men: list[str],
):
    # Create Gmail API client
    service: Resource = build("forms", "v1", credentials=credentials)

    date: str = datetime.now().ctime()

    form: dict = {
        "info": {
            "title": "Outstanding Student Awards",
            "documentTitle": f"Outstanding Student Awards Form - {date}",
        }
    }

    update_form_requests: dict = {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {
                        "description": (
                            'Voting form for Outstanding Student Awards. Please select a student or enter a student of your choice in "Other" in each category.'
                        )
                    },
                    "updateMask": "description",
                },
            }
        ]
    }

    #Create question for freshman man
    f_man_a:list[dict] = []

    for freshman in freshman_men:
        f_man_a.append({"value": freshman})

    f_man_a.append({"isOther": True})

    f_man_q:dict = build_question_body("Outstanding Freshman Man", "Pick a candidate for Outstanding Freshman Man", True, "RADIO", f_man_a, True)

    f_woman_a:list[dict] = []

    for freshman in freshman_women:
        f_woman_a.append({"value": freshman})

    f_woman_a.append({"isOther": True})

    # Append this request to create question
    update_form_requests["requests"].append(f_man_q)

    # Create form
    result = service.forms().create(body=form).execute()

    # Add questions
    question_setting = (
        service.forms()
        .batchUpdate(formId=result["formId"], body=update_form_requests)
        .execute()
    )

    get_result = service.forms().get(formId=result["formId"]).execute()

    print(get_result)


def build_question_body(
    title: str,
    description: str,
    required: bool,
    type: str,
    options: list[dict],
    shuffle: bool,
) -> dict:

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
                            "shuffle": True,
                        },
                    }
                },
            },
            "location": {"index": 0},
        }
    }

    return question_body


if __name__ == "__main__":
    from rich import print

    creds = google_oauth()

    create_form(creds, ["Angel", "Angel2"], None, None, None, None, None, None)
