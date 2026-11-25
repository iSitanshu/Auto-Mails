
import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

print("EMAIL AUTOMATION STARTED")

# Email credentials
your_email = os.getenv("EMAIL")
your_password = os.getenv("EMAIL_PASSWORD")

if not your_email or not your_password:
    raise ValueError("Email credentials not found in .env file")

# Load email template
with open("email_template.txt", "r", encoding="utf-8") as file:
    email_template = file.read()

# Read HR data from CSV
with open("hr_data.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    hr_data = list(reader)


# Function to send email
def send_email(to_email, subject, body):

    msg = MIMEMultipart()
    msg["From"] = your_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(your_email, your_password)
            server.sendmail(your_email, to_email, msg.as_string())

        print(f"Email successfully sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")


# Loop through HR data and send emails
for hr in hr_data:

    hr_name = hr["HR Name"].strip()
    hr_email = hr["HR Email"].strip()
    company_name = hr["Company Name"].strip()

    if not hr_email:
        print(f"Skipping {company_name}: Missing HR email")
        continue

    # Personalize email
    subject = f"Application for SDE-1 Role at {company_name}"

    body = email_template.replace("[XYZ Company]", company_name)
    body = body.replace("[Sir/Ma'am]", hr_name if hr_name else "Sir/Ma'am")

    # Send email
    send_email(hr_email, subject, body)

print("EMAIL AUTOMATION COMPLETED")
