# https://developers.google.com/gmail/api/quickstart/python
import os.path
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauthlib.oauth2.rfc6749.errors import AccessDeniedError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/forms.body",
]


class OAuthTimedOutError(Exception):
    """Exception that occurs when Google OAuth consent page times out."""


class OAuthAccessDeniedError(AccessDeniedError):
    """Exceptions that occurs access is denied on Google OAuth consent page."""


def google_oauth() -> Credentials:
    """Gets authorization from token on user from Google OAuth consent page, then returns credentials.

    Returns:
        Credentials: Credentials needed for communicating with Google APIs.
    """
    creds: Credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except ValueError as e:
            creds = None
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # If credentials are available, but expired, try to refresh the token.
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            # If refresh error occurs, let the user log in.
            except:
                creds = __try_get_creds("credentials.json", SCOPES, 60)
        else:
            creds = __try_get_creds("credentials.json", SCOPES, 60)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def __try_get_creds(
    client_secrets_file: str, scopes: list[str], timeout_seconds: int = None
) -> Credentials:
    """Displays the Google OAuth Consent Page for prompting user give Scholarly certain permissions.

    Args:
        client_secrets_file (str): File path to client secrets file.
        scopes (list[str]): The requested permissions / scopes the user is to allow for Scholarly.
        timeout_seconds (int, optional): The amount of time in seconds for the Google OAuth consent page times out. Defaults to None, which is no timeout.

    Raises:
        OAuthTimedOutError: Raised when Google OAuth consent page times out.
        OAuthAccessDeniedError: Raised when the user denies Scholarly access to necessary permissions.

    Returns:
        Credentials: Credentials needed for using Google APIs.
    """
    creds: Credentials = None

    flow:InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)

    # Show consent page, and attempt to get credentials
    try:
        creds = flow.run_local_server(
            timeout_seconds=timeout_seconds, authorization_prompt_message=None
        )
    except AttributeError as e:
        raise OAuthTimedOutError(
            "Google OAuth consent page timed out or authentication failed. Please try again."
        )
    except AccessDeniedError as a:
        raise OAuthAccessDeniedError(
            "Google OAuth consent was denied. Please try again and allow Scholarly access."
        )

    return creds


if __name__ == "__main__":
    from rich import print
    try:
        creds = google_oauth()
        print(creds.__dict__)
    except OAuthTimedOutError as e:
        print(e)
    except OAuthAccessDeniedError as a:
        print(a)
