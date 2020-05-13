import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, Rec):
        self.Port = 465
        self.Sender = ""
        self.Password = ""
        self.Receiver = Rec

    def CreateMessage(self, Password):
        self.Message = MIMEMultipart("Plain")
        self.Message['From'] = self.Sender
        self.Message['To'] = self.Receiver
        self.Message['Subject'] = "Resetowanie hasła"

        PlainText = """\
        Hello!
        This is your new password: {0}
        Best regards,
        MyLeader team.
        """.format(Password)

        PlainMess = MIMEText(PlainText, "plain")
        self.Message.attach(PlainMess)

    def SendMail(self):
        Context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", self.Port, context=Context) as EmailServer:
            EmailServer.login(self.Sender, self.Password)
            EmailServer.sendmail(self.Sender, self.Receiver, self.Message.as_string())
