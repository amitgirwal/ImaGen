from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, name, password=None, password2=None):
        """
            Creates and saves a User with the given email, name, password and password2.
            @param username:  the name for the new user
            @param password:  the password for the new user. if none is provided a random password is generated
            @param person:    the corresponding person object for this user
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        if not username:
            raise ValueError('User must have a valid username')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password=None, password2=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username=username,
            name=name,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True,
    )
    
    username = models.CharField(max_length=32, unique=True)

    name = models.CharField(max_length=255)
    photo = models.ImageField(default='user.png', upload_to='images/')
    bio = models.CharField(max_length=255, default='In Space 🚀', blank=True)
    url = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# Feedback
class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Subscribe
class Subscribe(models.Model):
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.email} | {self.created_at}"