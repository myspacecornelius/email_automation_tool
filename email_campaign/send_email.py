import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os

# SMTP Configuration
SMTP_SERVER = 'Add outgoing server'
SMTP_PORT = 587
EMAIL_ADDRESS = 'Add your email'
EMAIL_PASSWORD = 'add your password here'
SENDER_NAME = 'Test Email programs'

# Email sending function
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = f'{SENDER_NAME} <{EMAIL_ADDRESS}>'
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")

# Load emails from CSV in the external folder
def load_emails_from_csv(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df['email_ids'].tolist()
    else:
        print(f"Error: The file {file_path} does not exist.")
        return []

# Email body content
email_body = """
<div style="background-color: #f8f9fa; padding: 20px; font-family: Arial, sans-serif; color: #333;">
    <p>Hi,</p>

    <p>Looking to empower your email?</p>

    <p>Holaaaaaa</p>

    <p>Set up a time that works best for you.</p>

    <p>Best regards,<br><br>
</div>
"""

# Main function to send emails
def main():
    # Define the path to the external emails.csv file
    external_folder = os.path.join('..', 'common_data')  # Adjust this path if needed
    emails_file = os.path.join(external_folder, 'emails.csv')

    # Load the emails from the external CSV file
    email_list = load_emails_from_csv(emails_file)

    if email_list:
        # Update the subject to the desired format
        subject = 'Test email'

        # Send emails
        for email in email_list:
            send_email(email, subject, email_body)
    else:
        print("No emails to send.")

if __name__ == '__main__':
    main()
