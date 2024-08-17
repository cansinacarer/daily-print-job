import smtplib
import requests
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv


try:
    # Load environment variables from .env file for local testing
    from dotenv import load_dotenv

    load_dotenv()
except:
    # Error handling for the serverless function where it doesn't work, nor is it needed
    pass


def send_email():
    # Sender details
    sender_email = getenv("SENDER_EMAIL")
    password = getenv("SENDER_PASSWORD")
    smtp_server = getenv("SMTP_SERVER")
    port = getenv("PORT")

    # Email details
    recipient_email = getenv("RECIPIENT_EMAIL")
    subject = "Print Job"
    body = ""

    # Remote file URL
    file_url = "https://github.com/cansinacarer/daily-print-job/blob/main/printer_test_job_test_page.pdf?raw=true"
    local_filename = "printer_test_job_test_page.pdf"

    # Download the file
    response = requests.get(file_url)
    with open(local_filename, "wb") as f:
        f.write(response.content)

    # Open PDF file in binary mode
    with open(local_filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message["Bcc"] = recipient_email

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {local_filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, text)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")


def main():
    # Call the function to send the email
    send_email()
