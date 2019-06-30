import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(configurations, transferred_success, amount):
    message = MIMEMultipart()
    message["From"] = configurations.get("email_notifications").get("sender_email")
    message["To"] = configurations.get("email_notifications").get("recipient_email")
    message["Subject"] = f"Successfully transferred {amount} from 10bis to Segev" if transferred_success else "No balance remaining to transfer from 10bis to segev" if amount <= 0 else "Failed to transfer from 10bis to Segev"

    body = "attached logs for 10bis to Segev python script"
    message.attach(MIMEText(body, "plain"))

    filename = "output.txt"
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")

    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(configurations.get("email_notifications").get("sender_email"), configurations.get("email_notifications").get("sender_mailbox_password"))
        server.sendmail(configurations.get("email_notifications").get("sender_email"), configurations.get("email_notifications").get("recipient_email"), text)
