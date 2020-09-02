from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField

# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model as user_model
# User = user_model()


# Create your models here.
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, firstname, lastname, phone_num, password=None):
        """Create a new user profile"""
        if not firstname:
            raise ValueError("Users must have a name")
        if not email:
            raise ValueError("Users must have an email address")
        if not phone_num:
            raise ValueError("Users must have a phone number")

        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, phone_num=phone_num)
        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_superuser(self, email, firstname, lastname, phone_num, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, firstname, lastname, phone_num, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    firstname = models.CharField("First Name", max_length=25, blank=False, null=False)
    lastname = models.CharField("Last Name", max_length=25, blank=True)
    #Blank determines whether the field is required or not when creating an object
    #Charfield and Textfield are never stored as NULL in the database since it will have an empty string
    email = models.EmailField("Email", max_length=50, unique=True, blank=False, null=False)
    phone_num = PhoneNumberField("Phone Number", null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phone_num']

    # def get_full_name(self):
    #     """Retrieve full name of user"""
    #     return self.name
    #
    # def get_short_name(self):
    #     """Retrieve short name of user"""
    #     return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email


# class ExtraInfo(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='./static/defaul.png/')
