from django.contrib.auth import get_user_model
User = get_user_model()

class UserRepository:
    @staticmethod
    def get_by_email(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def create_user(**kwargs):
        return User.objects.create(**kwargs)

    @staticmethod
    def save(user):
        user.save()
        return user
