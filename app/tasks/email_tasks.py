from app.celery_app import celery
from app.emails import send_email


@celery.task
def send_welcome_email(to_email: str):
    """
    Runs in the background after a new user registers.
    """

    subject = "Welcome to CRUDPROD"

    body = f"""
    <h2>Welcome to CRUDPROD!</h2>

    <p>Thank you for joining our community.</p>

    <p>We're excited to have you.</p>

    <br>

    <p>The CRUDPROD Team</p>
    """

    send_email(
        to_email=to_email,
        subject=subject,
        body=body,
    )


@celery.task
def send_password_reset_email(
    to_email: str,
    reset_link: str,
):
    """
    Sends a password reset email.
    """

    subject = "Reset your password"

    body = f"""
    <h2>Password Reset</h2>

    <p>Click the button below to reset your password.</p>

    <a href="{reset_link}">
        Reset Password
    </a>
    """

    send_email(
        to_email=to_email,
        subject=subject,
        body=body,
    )


@celery.task
def send_verification_email(
    to_email: str,
    verification_link: str,
):
    """
    Sends an email verification link.
    """

    subject = "Verify your Email"

    body = f"""
    <h2>Email Verification</h2>

    <p>Click below to verify your account.</p>

    <a href="{verification_link}">
        Verify Email
    </a>
    """

    send_email(
        to_email=to_email,
        subject=subject,
        body=body,
    )


@celery.task
def send_notification_email(
    to_email: str,
    actor_email: str,
):
    """
    Sends an email when another user interacts with you.
    """

    subject = "New Notification"

    body = f"""
    <h2>You have a new notification.</h2>

    <p>{actor_email} interacted with your account.</p>
    """

    send_email(
        to_email=to_email,
        subject=subject,
        body=body,
    )