import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
import os
from twilio.rest import Client
    
def send_email(usersEmail, usersName, doctorsName):
    # usersEmail - User's email address
    # usersName - User's first and last name concatenated
    # doctorsName - Doctor's last name
    # message - message to send to usersEmail from doctor

    # send from this gmail email
    gmail_user = os.environ["GMAIL_EMAIL"] 
    gmail_password = os.environ["GMAIL_PASSWORD"] 
    # open smtp server
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_password)

    # compose email message
    msg = MIMEText("Happy birthday {} from Dr. {}!".format(usersName, doctorsName))
    msg['Subject'] = "Happy birthday!"
    msg['From'] = gmail_user 
    msg['To'] = usersEmail 

    # send email and stop server
    smtpserver.sendmail(gmail_user, [usersEmail], msg.as_string())
    smtpserver.quit()

##  Sends message over email to user from doctor (message most likely 'happy birthday')  
    
def send_text(usersNumber, usersName, doctorsName):
    # usersNumber - User's phone number (note: need to clean number to '+1**********', assuming USA based)
    # usersName - User's first and last name concatenated
    # doctorsName - Doctor's last name
    # message - message to send to usersEmail from doctor
    ###  Sends message over sms to user from doctor (message most likely 'happy birthday')  
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    
    client = Client(account_sid, auth_token)
    
    # send message with twilio
    client.messages.create(
        to= usersNumber,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        body="Happy birthday {} from Dr. {}!".format(usersName, doctorsName)
    )




    
