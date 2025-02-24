from django.core.mail import send_mail
from django.conf import settings

def send_email_token(email, token, username):
    try:
            subject = "Your account needs to be verifeid."
            message = f"""Hey {username},

            Thank you for signing up for OwlAi!
            To complete your registration and secure your account, 
            please verify your email address by clicking the link below:

            Verify: http://127.0.0.1:8000/verify/{token}/ 

            If you did not sign up for OwlAi Blog Generator, please ignore this email.

            Best regards,  
            OwlAi Team"""

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Email error: {e}")  # For debugging
        return False
    return True