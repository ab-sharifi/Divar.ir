from divar import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to,code):
    message = MIMEMultipart()
    message['from'] = config.EMAIL_USERNAME
    message['to'] = to
    message['subject'] = "Divar Code"
    message.attach(MIMEText(f"کاربرگرامی کد تایید شما در دیوار {code} می باشد"))

    try:
        with smtplib.SMTP(host="mail.ali-sharify.ir", port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(config.EMAIL_USERNAME,config.EMAIL_PASSWORD)
            smtp.send_message(message)
    except:
        return False
    else:
        return True


