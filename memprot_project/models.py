import uuid

from django.contrib.auth.models import AbstractBaseUser, User, UserManager, PermissionsMixin
from django.db import models



from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import update_last_login

user_logged_in.disconnect(update_last_login)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    # Links UserProfile to a User model instance
    objects = UserManager()

    # The additional attributes we wish to include
    username = models.CharField(max_length=100, default='some_rando', primary_key=True)
    institution = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    last_login = models.DateField(null=True)
    job_priority = models.IntegerField(default=-100)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email', 'institution']

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.username

