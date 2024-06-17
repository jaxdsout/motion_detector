import os
import smtplib
import mimetypes
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()
APP_KEY = os.getenv("GMAIL_APP_KEY")
SENDER = os.getenv("GMAIL_ADDRESS")
RECEIVER = os.getenv("GMAIL_ADDRESS")


def send_email(filepath):
    email = EmailMessage()
    email["Subject"] = "thing detected!"
    email.set_content("please see the attached screen shot for motion alert")

    with open(filepath, "rb") as file:
        content = file.read()
    # adds the binary content of the target capture, sets the file type to be rendered
    mime_type, _ = mimetypes.guess_type(filepath)
    maintype, subtype = mime_type.split('/')

    email.add_attachment(
        content,
        maintype=maintype,
        subtype=subtype,
        filename=os.path.basename(filepath)
    )

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, APP_KEY)
    gmail.sendmail(SENDER, RECEIVER, email.as_string())
    gmail.quit()


if __name__ == '__main__':
    send_email(filepath="images/image-10.png")
