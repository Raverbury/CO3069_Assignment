import smtplib
import ssl
import config


def send_alert_email():
    port = 465  # For SSL

    smtp_server = "smtp.gmail.com"
    sender_email = config.sender_email
    receiver_email = config.recipient_email
    password = config.sender_password
    message = """\
    Subject: Hi there

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
