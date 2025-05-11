import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials
your_email = "sitanshumishra18@gmail.com"  # Replace with your email
your_password = "liut rgxq dzbz yrez"  # Replace with your email password

# Load the email template
with open("email_template.txt", "r") as file:
    email_template = file.read()

# Read HR data from CSV
with open("hr_data.csv", "r") as file:
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
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Use Gmail's SMTP server
            server.starttls()
            server.login(your_email, your_password)
            server.sendmail(your_email, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Loop through HR data and send emails
for hr in hr_data:
    hr_name = hr["HR Name"]
    hr_email = hr["HR Email"]
    company_name = hr["Company Name"]

    # Personalize the email
    subject = f"Application for SDE-1 Role at {company_name}"
    body = email_template.replace("[XYZ Company]", company_name)  # Replace company name
    body = body.replace("[Sir/Ma'am]", hr_name)  # Replace greeting with HR's name

    # Send the email
    send_email(hr_email, subject, body)