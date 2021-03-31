from datetime import datetime, timedelta
from twilio.rest import Client
from smtplib import SMTP_SSL

import os

gmail_user = os.getenv("SMTP_ACCOUNT_USERNAME")
gmail_password = os.getenv("SMTP_ACCOUNT_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")

sent_from = gmail_user
to = [receiver_email]

email_format = """\
From: %s
To: %s
Subject: %s

%s
"""


class EmailAlerter:
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
        self.last_sent_alert = None

    def send_alert(self):
        cur_time = datetime.now()
        if (
            self.last_sent_alert is None
            or self.last_sent_alert + timedelta(hours=1) < cur_time
        ):
            send_email(self.subject, self.body)
            send_text(f"{self.subject}.\n{self.body}")
            self.last_sent_alert = cur_time
        else:
            print("wouldnt sent email")


def send_email(subject, body):
    with SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.ehlo()
        smtp.login(gmail_user, gmail_password)

        email_text = email_format % (
            sent_from,
            ", ".join(to),
            subject,
            body,
        )
        smtp.sendmail(sent_from, to, email_text)


twilio_account_id = os.getenv("TWILIO_ACCOUNT_ID")
twilio_account_token = os.getenv("TWILIO_ACCOUNT_TOKEN")
sms_from_number = os.getenv("SMS_FROM_NUMBER")
sms_to_number = os.getenv("SMS_TO_NUMBER")


def send_text(body):
    client = Client(twilio_account_id, twilio_account_token)
    client.messages.create(to=sms_to_number, from_=sms_from_number, body=body)
