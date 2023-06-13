from django.db import models
import django.contrib.auth.models as auth_models
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):

    def _user_creation(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('User must have an email adress')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        return user

    def create_user(self, email, first_name, last_name, password=None):
        user = self._user_creation(email, first_name, last_name, password=None)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self._user_creation(email, first_name, last_name, password=None)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(auth_models.AbstractUser):
    """Models utilisateurs utiliser pour gérer l'authentification"""
    username = None

    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('email adresse', unique=True)
    password = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
