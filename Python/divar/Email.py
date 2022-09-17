from divar import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to,code):
    message = MIMEMultipart()
    message['from'] = config.EMAIL_USERNAME
    message['to'] = to
    message['subject'] = "کد تایید دیوار"
    message.attach(MIMEText(f"کاربرگرامی کد تایید شما در دیوار {code} \n از در دسترس قرار دادن کد در اخیتار دیگران جداا خودداری کنید می باشد"))

    try:
        with smtplib.SMTP(host="ali-sharify.ir", port=config.MAIL_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(config.EMAIL_USERNAME,config.EMAIL_PASSWORD)
            
            smtp.send_message(message)
    except Exception as e:
        print(e)
        return False
    else:
        return True


# from divar import config
# from divar import app,mail



# def send_email(to,code):
#     print(mail)
#     print(mail.state)
#     print(mail.app.config)
#     print(dir(mail))
#     sender = "divar-test@ali-sharify.ir"
#     recipients=to
#     subject="کد تایید دیوار"
#     body=f"کد تایید شما {code}"
#     mail.send_message(sender=sender,recipients=recipients,subject=subject,body=body)
