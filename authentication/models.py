from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager)
from datetime import datetime, timedelta
from utils.models import BaseAbstractModel
from utils.managers import CustomQuerySet


class UserManager(BaseUserManager):
    """
    We need to override the `create_user` method so that users can
    only be created when all non-nullable fields are populated.
    """

    def create_user(
            self,
            first_name=None,
            last_name=None,
            email=None,
            password=None,
            role='BY'
    ):
        """
        Create and return a `User` with an email, first name, last name and
        password.
        """

        if not first_name:
            raise TypeError('Users must have a first name.')

        if not last_name:
            raise TypeError('Users must have a last name.')

        if not email:
            raise TypeError('Users must have an email address.')

        if not password:
            raise TypeError('Users must have a password.')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=self.normalize_email(email))
        user.set_password(password)
        user.role = role
        user.save()
        return user

    def create_superuser(
            self, first_name=None, last_name=None, email=None, password=None):
        """Create a superuser"""
        if not first_name:
            raise TypeError('Superusers must have a first name.')

        if not last_name:
            raise TypeError('Superusers must have a last name.')

        if not email:
            raise TypeError('Superusers must have an email address.')

        if not password:
            raise TypeError('Superusers must have a password.')

        user = self.model(
            first_name=first_name, last_name=last_name,
            email=self.normalize_email(email), role='LA')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.set_password(password)
        user.save()


class User(AbstractUser, BaseAbstractModel):
    """This class defines the User model"""

    ROLES = (
        ('BA', 'BROKER ADMIN'),
        ('BC', 'BROKER OWNER'),
        ('BB', 'BROKER CLIENT'),
    )

    username = models.CharField(
        null=True, blank=True, max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        verbose_name='user role', max_length=2, choices=ROLES,
        default='BY'
    )
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    active_objects = CustomQuerySet.as_manager()

    def __str__(self):
        return f'{self.email}'
