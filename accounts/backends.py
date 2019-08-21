from django.db.models import Q
from accounts.models import User


class EmailOrUsernameAuthBackend(object):
    """
    Custom Backend to perform authentication via email OR username
    """
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(Q(username__iexact=email) | Q(email__iexact=email))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
