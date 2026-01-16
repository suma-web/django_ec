import os
import requests

def send_mailgun_message(to_email, subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxb9abe36b8e3d49a9bde83ecfc51667e7.mailgun.org/messages",
        auth=("api", os.environ["MAILGUN_API_KEY"]),
        data={
            "from": "Mailgun Sandbox <postmaster@sandboxb9abe36b8e3d49a9bde83ecfc51667e7.mailgun.org>",
            "to": to_email,
            "subject": subject,
            "text": text,
        }
    )
