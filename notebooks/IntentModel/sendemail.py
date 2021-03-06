from email.utils import COMMASPACE, formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase, MIMEText
from email import encoders
import os.path as op
import smtplib


def send_email(send_from, send_to, subject, message, files=[],
              server='', port='', username='', password='',
              use_tls=True):

    """
       Compose and send email with provided info and attachments

       args:
            send_from (str): from name
            send_to (str): to name
            subject (str): message title
            message (str): message body
            files (list[str]): list of file paths to be attached to email
            server (str): mail server host name
            port (int): port number
            username (str): server auth username
            password (str): server auth password
            use_tls (bool): use TLS mode
    """

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', 'octet-stream')
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)

    #smtp = smtplib.SMTP('smtp.gmail.com: 587')
    smtp = smtplib.SMTP(server, port)

    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
