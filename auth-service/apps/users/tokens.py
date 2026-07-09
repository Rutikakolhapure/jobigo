from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

def get_token_serializer():
    return URLSafeTimedSerializer(settings.SECRET_KEY, salt='auth-svc')

def make_token(payload):
    s = get_token_serializer()
    return s.dumps(payload)

def loads_token(token, max_age=60*60*24):  # default 1 day
    s = get_token_serializer()
    return s.loads(token, max_age=max_age)
