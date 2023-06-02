from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from authentification.models import User


# class SettingsBackend(BaseBackend):

#     def authenticate(self, request, email=None, password=None):
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return None
#         pwd_valid = check_password(password, user['password'])
#         if not pwd_valid:
#             return None
#         return user
        
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None