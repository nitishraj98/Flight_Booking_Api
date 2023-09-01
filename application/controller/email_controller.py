from application.controller import *


# Function to send registration email
def send_registration_email(email, name):
    sender_email = app.config['SENDER_EMAIL']
    sender_password = app.config['SENDER_PASSWORD']
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome to Anrari - Your Flight Booking Platform"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"""
   <!DOCTYPE html>  
<html lang="en">
<head>
    <meta charset="UTF-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Anrari - Flight Booking</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">

    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
        <tr>
            <td bgcolor="#FFA500" style="padding: 40px 0; text-align: center; color: #ffffff;">
                <h1>Welcome to Anrari!</h1>
                <p style="font-size: 18px;">Your Journey Begins Now</p>
            </td>
        </tr>
        <tr>
            <td bgcolor="#ffffff" style="padding: 40px;">
                <h2 style="color: #FFA500;">Dear {name},</h2>
                <p>Thank you for registering on Anrari - Your Flight Booking Platform. We are excited to have you on board!</p>
                <p>Start exploring our platform to discover the best flight deals and plan your next adventure with ease.</p>
                <a href="[Your Website URL]" style="display: inline-block; padding: 10px 20px; background-color: #FFA500; color: #ffffff; text-decoration: none; border-radius: 5px;">Start Exploring</a>
            </td>
        </tr>
        <tr>
            <td bgcolor="#f4f4f4" style="text-align: center; padding: 20px 0; color: #888888;">
                <p>Best regards,<br>Your Anrari Team</p>
                <p>Contact us at <a href="mailto:support@anrari.com">support@anrari.com</a></p>
            </td>
        </tr>
    </table>

</body>
</html>


    """

    part = MIMEText(html, "html") 
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())


