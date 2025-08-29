import os
import smtplib
from email.mime.text import MIMEText




def send_email(subject: str, body: str):
provider = (os.getenv("EMAIL_PROVIDER") or "gmail").lower()
to_addr = os.getenv("EMAIL_TO")
if not to_addr:
return


if provider == "sendgrid":
# via SMTP SendGrid
api_key = os.getenv("SENDGRID_API_KEY")
from_addr = os.getenv("EMAIL_FROM") or "no-reply@radar-esg"
if not api_key:
return
msg = MIMEText(body, "plain", "utf-8")
msg["Subject"] = subject
msg["From"] = from_addr
msg["To"] = to_addr
with smtplib.SMTP("smtp.sendgrid.net", 587) as s:
s.starttls()
s.login("apikey", api_key)
s.sendmail(from_addr, [to_addr], msg.as_string())
return


# Default: Gmail com App Password
from_addr = os.getenv("EMAIL_FROM")
app_pw = os.getenv("EMAIL_APP_PASSWORD")
if not (from_addr and app_pw):
return
msg = MIMEText(body, "plain", "utf-8")
msg["Subject"] = subject
msg["From"] = from_addr
msg["To"] = to_addr
with smtplib.SMTP("smtp.gmail.com", 587) as server:
server.starttls()
server.login(from_addr, app_pw)
server.sendmail(from_addr, [to_addr], msg.as_string())
