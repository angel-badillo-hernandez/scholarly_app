"""Provides fuctions and descriptive exceptions for using Google OAuth

This module provides functions for authenticating with Google OAuth and receiving credentials
that can be used to work with the GMail and Google Forms APIs.

Portions of code adapted from GMail API quickstart:
https://developers.google.com/gmail/api/quickstart/python
"""

import os.path
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from oauthlib.oauth2.rfc6749.errors import AccessDeniedError

# The allowed scopes for Google APIs to be used
SCOPES: list[str] = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/forms.body",
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]

# Absolute path for file to prevent issues with
# relative path when building app with PyInstaller
BASE_DIR: str = os.path.dirname(__file__)

# Absolute path for client secret JSON file
CLIENT_SECRET_FILE: str = os.path.join(
    BASE_DIR, f"assets\\google_auth\\credentials.json"
)

# Absolute path for token JSON file
TOKEN_FILE: str = os.path.join(BASE_DIR, f"assets\\google_auth\\token.json")


class OAuthTimedOutError(Exception):
    """Exception that occurs when Google OAuth consent page times out."""


class OAuthAccessDeniedError(AccessDeniedError):
    """Exceptions that occurs access is denied on Google OAuth consent page."""


class UserEmailAddressUnavailableError(Exception):
    """Exception that is raised when the user's email address is not obtainable."""


def google_oauth(time_out_seconds: int = 300) -> Credentials:
    """Gets authorization from token of user from Google OAuth consent page, then returns credentials.

    Args:
        time_out_seconds (int): The amount of time in seconds for the Google OAuth consent page times out. Defaults to 300, or 5 minutes. When None, there is no timeout.

    Returns:
        Credentials: Credentials needed for communicating with Google APIs.
    """
    creds: Credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
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
                creds = __try_get_creds(CLIENT_SECRET_FILE, SCOPES, time_out_seconds)
        else:
            creds = __try_get_creds(CLIENT_SECRET_FILE, SCOPES, time_out_seconds)
        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
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

    flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )

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


def get_user_email_address(credentials: Credentials) -> str:
    """Returns the current user's email address.

    Args:
        credentials (Credentials): The credentials retrieved from the OAuth token / login.

    Returns:
        str: The user's email address.
    """
    primary_email: str = None
    service = build("people", "v1", credentials=credentials)

    # Call the People API to get the authenticated user's primary email address.
    profile = (
        service.people()
        .get(resourceName="people/me", personFields="emailAddresses")
        .execute()
    )

    # Retreive primary email address
    email_addresses = profile.get("emailAddresses", [])
    if email_addresses:
        primary_email = next(
            (
                email["value"]
                for email in email_addresses
                if email.get("metadata", {}).get("primary", False)
            ),
            None,
        )

    # If the email address is None, that means the email address was not obtained
    if primary_email is None:
        raise UserEmailAddressUnavailableError(
            "Authenticated user's primary email address was not obtainable. Please try again."
        )

    return primary_email


if __name__ == "__main__":
    from rich import print

    try:
        creds = google_oauth()
        print(creds.to_json())
        email = get_user_email_address(creds)
        print(email)
    except OAuthTimedOutError as e:
        print(e)
    except OAuthAccessDeniedError as a:
        print(a)
    except UserEmailAddressUnavailableError as u:
        print(u)
