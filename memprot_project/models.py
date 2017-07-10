import uuid

from django.contrib.auth.models import AbstractBaseUser, User, UserManager, PermissionsMixin
from django.db import models




class UserProfile(AbstractBaseUser, PermissionsMixin):
    # Links UserProfile to a User model instance
    objects = UserManager()

    # The additional attributes we wish to include
    username = models.CharField(max_length=100, default='s08    fhc 2', unique=True)
    institution = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    job_priority = models.IntegerField(default=-100)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email', 'institution']

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

