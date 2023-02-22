from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Custom user manager
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)  # Function comes from superclass
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)  # In case of different database use

        return user

    def create_super_user(self, email, name, password):
        """Create and save a super user with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True  # It automotically created by PermissionMixin
        user.is_staff = True
        user.save(using=self._db)

        return user

# Custom user model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system"""
    # User fields. Django will use metaclass info to create user model
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()  # We set the manager for this here

    # For authentication
    USERNAME_FIELD = 'email'  # We are assigning username field to email to use email instead of username
    REQUIRED_FIELDS = ['name']

    # Couple of functions for our django to interact with our custom user UserProfile
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Retrun string representation of our user"""
        return self.email
