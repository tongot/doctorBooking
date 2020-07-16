from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from bookings.models import Patient
import datetime


class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, password=None):
        if not email:
            raise ValueError("User must have an Email address")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not date_of_birth:
            raise ValueError("User must have a date of birth")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
     
        
    def user_exist(self,email):
        return self.filter(email=email)

    def create_user_external(self,email,first_name,last_name, date_of_birth, gender, phone_number, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth, 
            password=password,
        )
        user.gender=gender
        user.is_staff = True
        user.phone_number=phone_number
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField(verbose_name="date of birth")
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    GENDER = (
            ("M", "MALE"),
            ("F", "FEMALE")
    )
    gender = models.CharField(choices=GENDER, max_length=1, default='MALE', blank=True, null=True)

    @property
    def age(self):
        return self.date_of_birth - datetime.date.today()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
