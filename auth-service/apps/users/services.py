from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from .tokens import make_token, loads_token
from django.contrib.auth import get_user_model
User = get_user_model()

def send_verification_email(user):
    token = make_token({'user_id': str(user.id), 'email': user.email})
    url = f"{settings.SITE_URL}/verify-email/?token={token}"
    send_mail(
        subject='Verify your JobiGo account',
        message=f'Click to verify your account: {url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    return token

def send_password_reset_email(user):
    token = make_token({'user_id': str(user.id), 'email': user.email})
    url = f"{settings.SITE_URL}/reset-password/?token={token}"
    send_mail(
        subject='Reset your JobiGo password',
        message=f'Click to reset your password: {url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    return token

def verify_token(token, max_age=60*60*24):
    try:
        payload = loads_token(token, max_age=max_age)
        return payload
    except Exception:
        return None
