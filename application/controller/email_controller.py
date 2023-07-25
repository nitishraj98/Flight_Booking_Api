from application.controller import *

# Function to send registration email
def send_registration_email(email, name):
    sender_email = 'nitishtics@gmail.com'
    sender_password = 'uvbooqspotsjrcto'
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Thanks for Registering"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"""
    <html>
        <body>
            <p>Dear {name},</p>
            <p>Thank you for registering on Anrari.</p>
            <p>Best regards,</p>
            <p>Your Anrari Team</p>
        </body>
    </html>
    """

    part = MIMEText(html, "html") 
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
