import smtplib
from email.message import EmailMessage
import streamlit as st
import os

def send_email(recipient, subject, body, sender_email, sender_password, attachments):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)

    # Attach files
    for attachment in attachments:
        try:
            with open(attachment, 'rb') as file:
                file_data = file.read()
                file_name = os.path.basename(attachment)
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        except Exception as e:
            st.error(f"Error attaching file {attachment}: {str(e)}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            st.success(f"Email sent to {recipient}")
    except smtplib.SMTPException as e:
        st.error(f"SMTP Error sending email to {recipient}: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error sending email to {recipient}: {str(e)}")

def validate_email(email):
    # Simple email validation
    return '@' in email and '.' in email

def main():
    st.title("Bulk Email Sender (Gmail)")

    # Inform user about application-specific password and provide instructions
    st.markdown("""**Important:** This application requires an application-specific password for your Gmail account to send emails securely.

    Here's how to generate an application-specific password for this app:

    1. Go to your Google Account settings (https://myaccount.google.com/intro/security).
    2. Navigate to the "Security" section.
    3. Find the "App passwords" option (under "Signing in to other apps").
    4. Click on "App passwords" and then select "Select app" and "Other (Custom name)".
    5. Provide a descriptive name for the password, like "Python Email App".
    6. Click "Generate".

    **Once generated, copy the password securely. You'll need to enter this password in the app.**

    **Note:** For security reasons, do not store the application-specific password in the app's code.""")

    sender_email = st.text_input("Enter your Gmail address:", placeholder="your_email@gmail.com")
    sender_password = st.text_input("Enter your Gmail 'APPLICATION' password:", type="password", placeholder="Enter password securely")

    # Input email subject
    email_subject = st.text_input("Enter email subject:", placeholder="Enter subject here")

    # Input email addresses
    email_list = st.text_area("Enter email addresses (one per line)")
    email_list = [email.strip() for email in email_list.split('\n') if validate_email(email.strip())]

    # Inform user about invalid emails
    if len(email_list) == 0:
        st.warning("No valid email addresses found. Please check your input.")

    # Input email content
    email_content = st.text_area("Enter email content")

    # File uploader for attachments
    uploaded_files = st.file_uploader("Upload attachments (optional):", accept_multiple_files=True)
    attachment_paths = []
    for uploaded_file in uploaded_files:
        with open(uploaded_file.name, 'wb') as f:
            f.write(uploaded_file.getbuffer())
            attachment_paths.append(uploaded_file.name)

    if st.button("Send Emails"):
        if not sender_email or not sender_password:
            st.error("Please provide your Gmail address and application password.")
            return

        if len(email_list) == 0:
            st.error("Please provide at least one valid recipient email address.")
            return

        if not email_subject or not email_content:
            st.error("Please provide both subject and content for the email.")
            return

        for recipient in email_list:
            try:
                send_email(recipient, email_subject, email_content, sender_email, sender_password, attachment_paths)
            except Exception as e:
                st.error(f"Error sending email to {recipient}: {str(e)}")

if __name__ == "__main__":
    main()
