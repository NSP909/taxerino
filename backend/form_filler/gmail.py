import base64
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Define the scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def authenticate_gmail():
    """Authenticate and authorize the Gmail API using OAuth2."""
    creds = None
    # Check if token.json exists (stored credentials)
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If no valid credentials, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("../../../creds.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def send_pdf_via_gmail(pdf_path, recipient_email="rthippar@terpmail.umd.edu", subject="PDF Attachment", body="Please find the attached PDF."):
    """Sends a PDF file via Gmail API."""
    # Authenticate and authorize
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    # Create Email
    msg = MIMEMultipart()
    msg["to"] = recipient_email
    msg["subject"] = subject

    # Add email body
    msg.attach(MIMEText(body, "plain"))

    # Attach PDF
    with open(pdf_path, "rb") as pdf_file:
        attachment = MIMEBase("application", "pdf")
        attachment.set_payload(pdf_file.read())

    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
    msg.attach(attachment)

    # Encode as base64
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    message = {"raw": raw_message}

    # Send Email
    sent_message = service.users().messages().send(userId="me", body=message).execute()
    
    print(f"Email sent! Message ID: {sent_message['id']}")

# Example usage
# send_pdf_via_gmail("filled_w4.pdf", "rthippar@umd.edu")