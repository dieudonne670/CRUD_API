import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings


def send_email(
    to_email: str,
    subject: str,
    body: str,
):
    """
    Generic email sender.

    Every email in the project eventually
    comes through this function.
    """

    # -------------------------
    # Create email object
    # -------------------------

    message = MIMEMultipart()

    message["From"] = settings.email_username
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "html")
    )

    # -------------------------
    # Connect to SMTP
    # -------------------------

    server = smtplib.SMTP(
        settings.email_host,
        settings.email_port,
    )

    server.starttls()

    # -------------------------
    # Login
    # -------------------------

    server.login(
        settings.email_username,
        settings.email_password,
    )

    # -------------------------
    # Send
    # -------------------------

    server.sendmail(
        settings.email_username,
        to_email,
        message.as_string(),
    )

    server.quit()