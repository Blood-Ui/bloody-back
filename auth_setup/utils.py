import random
from django.core.mail import EmailMessage
import decouple
from .models import User, OneTimePassword


def generateOTP():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1, 9))
    return otp

def send_code_to_user(email):
    Subject = "One time passcode for Email verification"
    otp_code = generateOTP()
    print(otp_code)
    user = User.objects.get(email=email)
    current_site = "myAuth.com"
    email_body = f"Hi {user.first_name}, thanks for signing up on {current_site} please verify your email by entering the \n one time passcode: {otp_code}"
    from_email = decouple.config("FROM_MAIL")

    OneTimePassword.objects.create(user=user, code=otp_code)

    send_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    send_email.send(fail_silently=False)

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=decouple.config("FROM_MAIL"),
        to=[data['to_email']]
    )
    email.send()