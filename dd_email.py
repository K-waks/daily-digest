from tkinter import *
import dd_content
import pandas as pd
import datetime
import smtplib
import ssl
import config
from email.message import EmailMessage


class DailyDigestEmail:
    def __init__(self):
        self.content = {
            "verse": {"include": True, "content": dd_content.get_verse()},
            "weather": {"include": True, "content": dd_content.get_weather_forecast()},
            "devotions": {"include": True, "content": dd_content.get_devotion()},
            "wikipedia": {
                "include": True,
                "content": dd_content.get_wikipedia_article(),
            },
            "announcement": {"include": True, "content": True},
        }

        df = pd.read_sql("SELECT email FROM subscribers;", con=dd_content.engine)
        self.recipients_list = df["email"].tolist()

        self.sender_credentials = {
            "email": "wakskevin2ndyearproject@gmail.com",
            "password": "dd_password123",
        }

    """
    Generate email message body as HTML.
    """

    def format_digest(self):

        html = f"""
                <html>
                <body>
                    <center>
                        <h1>Daily Digest - {datetime.date.today().strftime('%d %b %Y')}</h1>
                """

        # TODO: format random verse
        if self.content["verse"]["include"] and self.content["verse"]["content"]:
            html += f"""
                        <h2>Verse of the Day</h2>
                        <i>"{self.content['verse']['content']['verse']}"</i> - {self.content['verse']['content']['reference']}
                """
        # TODO: format weather forecast
        if self.content["weather"]["include"] and self.content["weather"]["content"]:
            html += f"""
        <h2>Forecast for {self.content['weather']['content']['city']}, {self.content['weather']['content']['country']}</h2>
        <table>
                    """

            for forecast in self.content["weather"]["content"]["periods"]:
                html += f"""
            <tr>
                <td>
                    {forecast['timestamp'].strftime('%d %b %H%M')}
                </td>
                <td>
                    <img src="{forecast['icon']}">
                </td>
                <td>
                    {forecast['temp']}\u00B0C | {forecast['description']}
                </td>
            </tr>
                        """

            html += """
            </table>
                    """
        # TODO: format devotions
        if (
            self.content["devotions"]["include"]
            and self.content["devotions"]["content"]
        ):
            html += f"""
                        <h2>Today's devotions</h2>
                        <i>"{self.content['devotions']['content']['readings']}"</i> - {self.content['devotions']['content']['weekday']}
													"""

        # TODO: format Wikipedia article
        if (
            self.content["wikipedia"]["include"]
            and self.content["wikipedia"]["content"]
        ):
            html += f"""
             <h2>Daily Random Learning</h2>
             <h3><a href="{self.content['wikipedia']['content']['url']}">{self.content['wikipedia']['content']['title']}</a></h3>
             <table width="800">
            <tr>
                <td>{self.content['wikipedia']['content']['extract']}</td>
            </tr>
            </table>
                    """

        html += """
                    </center>
                </body>
                </html>
                """

        return {"html": html}

    def format_announcement(self):

        html = f"""
                <html>
                <body>
                    <center>
                        <h1>Treeolive Christian Fellowship - {datetime.date.today().strftime('%d %b %Y')}</h1>
                """

        # TODO: format random verse
        if (
            self.content["announcement"]["include"]
            and self.content["announcement"]["content"]
        ):
            import dd_gui

            self.content["announcement"]["content"] = dd_gui.value
            html += f"""
                        <h2>Church Announcements</h2>
                        "{self.content['announcement']['content']}"
                """
        html += """
                    </center>
                </body>
                </html>
                """

        return {"html": html}

    """
    Send digest email to all recipients on the recipient list.
    """

    def send_email_digest(self):
        # TODO: build email message
        msg1 = EmailMessage()
        msg1["Subject"] = f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        msg1["From"] = self.sender_credentials["email"]
        msg1["To"] = ", ".join(self.recipients_list)

        # TODO: add HTML content
        msg_body = self.format_digest()
        msg1.set_content(msg_body["html"], subtype="html")

        # TODO: secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(
                self.sender_credentials["email"], self.sender_credentials["password"]
            )
            server.send_message(msg1)

    """
    Send announcement email to all recipients on the recipient list.
    """

    def send_email_announcement(self):
        # TODO: build email message
        msg2 = EmailMessage()
        msg2["Subject"] = f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        msg2["From"] = self.sender_credentials["email"]
        msg2["To"] = ", ".join(self.recipients_list)

        # TODO: add HTML content
        msg_body = self.format_announcement()
        msg2.set_content(msg_body["html"], subtype="html")

        # TODO: secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(
                self.sender_credentials["email"], self.sender_credentials["password"]
            )
            server.send_message(msg2)


def test_module():

    # TODO: test format_message()
    print("\nTesting email body generation...")
    message = email.format_digest()

    print("\nHTML email body is...")
    print(message["html"])

    with open(f"{config.temp}/message.html", "w", encoding="utf-8") as f:
        f.write(message["html"])

    # TODO: test send_email()
    print("\nSending test email...")
    email.send_email_digest()


if __name__ == "__main__":
    email = DailyDigestEmail()
    test_module()
