import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional
from .config import GMAIL_USER, GMAIL_APP_PASSWORD, DEST_EMAIL

def send_email_with_attachments(subject: str, body: str, json_bytes: bytes, image_bytes: Optional[bytes], image_filename: str = "car.jpg"):
    if not (GMAIL_USER and GMAIL_APP_PASSWORD and DEST_EMAIL):
        raise RuntimeError("Email env vars missing. Set GMAIL_USER, GMAIL_APP_PASSWORD, DEST_EMAIL.")

    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = DEST_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # JSON attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(json_bytes)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="car_listing.json"')
    msg.attach(part)

    # Image attachment
    if image_bytes:
        img_part = MIMEBase("application", "octet-stream")
        img_part.set_payload(image_bytes)
        encoders.encode_base64(img_part)
        img_part.add_header("Content-Disposition", f'attachment; filename="{image_filename}"')
        msg.attach(img_part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, DEST_EMAIL, msg.as_string())
