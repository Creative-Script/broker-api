import os
import jwt
from broker.settings import EMAIL_HOST_USER, SECRET_KEY
from django.db.models.signals import post_save
from datetime import datetime, timedelta

from django.urls import reverse
from django.core.mail import send_mail

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, fname, lname, username, email, password=None):
        """
        Creates and returns a new user.
        params: first name, last or other names, username, password
        """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(fname=fname, lname=lname, username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, fname, lname, username, email, password):
        """
      Create the website admin
      """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(fname, lname, username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        db_index=True,
        max_length=255,
        unique=True
    )

    email = models.EmailField(
        db_index=True,
        unique=True
    )
    fname = models.CharField(
        max_length=255
    )
    lname = models.CharField(
        max_length=255
    )
    is_active = models.BooleanField(default=False)
    is_broker = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fname', 'lname']

    objects = UserManager()

    def __str__(self):
        """
        Returns string representation of current user object
        """
        return self.email

    @property
    def get_full_name(self):
        """
        This method returns user full name
        """
        return self.fname+" "+self.lname

    def get_short_name(self):
        """
        """
        return self.username

    @property
    def token(self):
        """
        sets user token
        """
        return self.generated_jwt_token()

    def generated_jwt_token(self):
        """
        Creates token that stores user email and id

        """
        exp_time = datetime.now() + timedelta(hours=3)
        token = jwt.encode({
            'id': self.pk,
            'email': self.email,
            'exp': int(exp_time.strftime('%s'))
        }, SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    @staticmethod
    def call_back(link):
        def fun(sender, instance, **kwargs):
            token = instance.generated_jwt_token()
            url = reverse('activate-user', kwargs={
                'token': token
            })

            domain = str(link) + str(url)
            send_mail(
                subject=instance.username + " Welcome to the Broker.",
                message="Welcome to Broker." +
                        "\nLogin using this link\nhttp://" + domain,
                from_email=EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=False)

        return fun

    @staticmethod
    def get_url(url):
        """
        Get the current url
        """
        post_save.connect(User.call_back(url), sender=User, weak=False)
