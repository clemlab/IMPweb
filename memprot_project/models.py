import uuid

from django.contrib.auth.models import AbstractBaseUser, User, UserManager, PermissionsMixin
from django.db import models

# LISTEN UP THIS IS BLOODY IMPORTANT:
# IT's OK TO ADD/REMOVE SOME FIELDS AS LONG AS YOU MIGRATE PROPERLY
# HOWEVER,
# MAKE SURE YOU READ THE DOCUMENTATION/OTHER CODE FIRST
# THIS IS A CUSTOM USER MODEL AND IS __NOT__ SIMPLE TO WORK WITH
# BECAUSE EVERYTHING ELSE TIES INTO IT SINCE MOST THINGS EXPECT/REQUIRE LOGIN
# BE CAREFUL AND ALLOW YOURSELF AN OUT (BACKUP) IF POSSIBLE

# EXAMPLE: THERE'S A LAST_LOGIN FIELD INHERITED FROM ABSTRACTBASEUSER THAT
#           DOESN'T APPEAR HERE. THE LOGIN PROCESS CARES ABOUT IT, SO DON'T
#           SCREW WITH IT UNLESS YOU'RE WILLING TO TAKE APART THAT WHOLE
#           FLOW. IF YOU SEE AN ERROR WITH IT IT'S LIKELY THAT YOU AREN'T
#           HANDLING THE USER MODEL CORRECTLY, AND NOT THAT YOU NEED TO
#           FIX THAT DATABASE TABLE.

# </endrant>


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

