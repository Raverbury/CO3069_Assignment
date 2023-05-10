import smtplib
import ssl
import config
from email.message import EmailMessage


def send_alert_email():
    port = 465  # For SSL

    smtp_server = "smtp.gmail.com"
    sender_email = config.GMAIL_SENDER_EMAIL
    receiver_email = config.RECIPIENT_EMAIL
    password = config.GMAIL_SENDER_PASSWORD
    body = f"""\
    Dear {receiver_email},

    We are writing to inform you that our application has detected changes on your website. This could be the result of a deface attack attempt on your website.

    If you did not make those changes, consider your website a victim of a deface attack and use a backup to restore it to a healthy state.
    If you did make those changes, consider updating the known state of your website and restart the detection program.

    Thank you for your attention to this matter.

    Sincerely,

    The DefaceCheck Team.
    """

    msg = EmailMessage()
    msg.set_content(body)

    msg['Subject'] = "Alert: Changes detected on your website"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()