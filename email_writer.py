# https://developers.google.com/gmail/api/quickstart/python
from scholarly_google_auth import get_user_email_address
from google.oauth2.credentials import Credentials
import base64
import mimetypes
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError


def gmail_send_email(
    credentials: Credentials,
    recipient_email_address: str,
    subject: str,
    body: str,
    attachment_path: str,
) -> None:
    """Send an email via Gmail from the authorized user's Google Account.

    Args:
        credentials (Credentials): Credentials needed to communicate with Google APIs.
        recipient_email_address (str): Email address of the recipient.
        subject (str): Subject of the email.
        body (str): Body of the email.
        attachment_path (str): File path to the attachment.
    """

    # Create Gmail API client
    service: Resource = build("gmail", "v1", credentials=credentials)
    email_message: EmailMessage = EmailMessage()

    # Headers
    email_message["To"] = recipient_email_address
    email_message["From"] = get_user_email_address(credentials)
    email_message["Subject"] = subject

    # Text content
    email_message.set_content(body)

    # Build attachment MIME part
    attachment_part = __build_attachment(attachment_path)

    # Add attachment part to the message
    email_message.add_attachment(
        attachment_part.get_payload(decode=True),
        maintype=attachment_part.get_content_maintype(),
        subtype=attachment_part.get_content_subtype(),
        filename=os.path.basename(attachment_path),
    )

    # Encode messaged for request body
    encoded_message: str = base64.urlsafe_b64encode(email_message.as_bytes()).decode()

    # Request body for GMail API
    send_email_request_body: dict = {"raw": encoded_message}

    # Perform API call and send email
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=send_email_request_body)
        .execute()
    )


def __build_attachment(file_path: str) -> MIMEText | MIMEAudio | MIMEImage | MIMEBase:
    """Create the MIME document for a file.

    Args:
        file_path (str): File path for the file attachment.

    Returns:
        MIMEText | MIMEAudio | MIMEImage | MIMEBase: An MIMEBase object representing the file.
    """
    # Get the content type for file
    content_type, _ = mimetypes.guess_type(file_path)

    # If content type could not be discerned, use
    # application/octet-stream to represent a generic binary file
    if content_type is None:
        content_type = "application/octet-stream"

    main_type, sub_type = content_type.split("/", 1)

    mime_document: MIMEBase = None

    # Open the file for reading as binary
    with open(file_path, "rb") as file:
        # If main type is text, create MIMEText document
        if main_type == "text":
            mime_document: MIMEText = MIMEText(file.read().decode(), _subtype=sub_type)
        # If main type is image, create MIMEImage document
        elif main_type == "image":
            mime_document: MIMEImage = MIMEImage(file.read(), _subtype=sub_type)
        # If main type is audio, create MIMEAudio document
        elif main_type == "audio":
            mime_document: MIMEAudio = MIMEAudio(file.read(), _subtype=sub_type)
        # If main type is not one of the common MIME types, create the appriopriate
        # document with MIMEBase
        else:
            mime_document: MIMEBase = MIMEBase(main_type, sub_type)
            mime_document.set_payload(file.read())

    # Get the file name from the file path
    filename: str = os.path.basename(file_path)

    # Add appriopriate header for the attachment
    mime_document.add_header("Content-Disposition", "attachment", filename=filename)

    return mime_document


if __name__ == "__main__":
    from scholarly_google_auth import google_oauth
    from datetime import datetime

    # Get credentials from Google OAuth
    creds = google_oauth()

    # Send email with the following data
    gmail_send_email(
        credentials=creds,
        recipient_email_address=get_user_email_address(creds),
        subject=f"Scholarly Email Test: {datetime.now().ctime()}",
        body="""
        Dear reader,

        This is a test. Sent from Scholarly 🥳.

        Regards,

        S.E.E.S (Software Engineering Execution Squad)
        Angel Badillo
        """,
        attachment_path="assets\\templates\\template_letter.docx",
    )
