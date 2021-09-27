from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.fields import CharField

import uuid
import os
from django.utils import timezone

def recipe_image_fiel_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4}.{ext}'

    return os.path.join('upload/recipe/', filename)


class UserManager(BaseUserManager):
     
    def create_user(self, username, password=None, **extra_fields):
      
        if not username:
            raise ValueError('User not have username')

        # email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,username, password):

        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False) # if True is doctor, if False is patient

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def get_item(self, *args, **kwargs):
        print('kwarg', kwargs)
        # print(args.type())
        if args[0] == 'username':
            return self.username
        elif args[0] == 'email':
            return self.email
        elif args[0] == 'name':
            return self.name
        elif args[0] == 'is_doctor':
            return self.is_doctor
        else:
            return self.id


class Doctor(models.Model):
    speciality = models.CharField(max_length=100)
    ubication = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to=recipe_image_fiel_path)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # primary_key=True
    )

    def __str__(self):
        return self.user.username

    def get_item(self, *args, **kwargs):
        print('kwarg', kwargs)
        # print(args.type())
        if args[0] == 'speciality':
            return self.speciality
        elif args[0] == 'ubication':
            return self.ubication
        elif args[0] == 'username':
            return self.user.username
        elif args[0] == 'name':
            return self.user.name
        elif args[0] == 'image':
            return self.image
        else:
            return self.id

class Patient(models.Model):
    name = models.CharField(max_length=255)
    sick = models.CharField(max_length=100)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # primary_key=True
    )
    doctor = models.ForeignKey(Doctor, related_name="patients", on_delete=models.PROTECT)
      
    def __str__(self):
        return self.name

class Petition(models.Model):
    phone = models.IntegerField()
    title = models.CharField(max_length=100)
    information = models.TextField(max_length=255, null=True)
    answer =models.TextField(max_length= 255, null=True)
    sick = models.CharField(max_length=25)
    age = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)   # auto
    patient  = models.ForeignKey(Patient, on_delete=models.PROTECT,primary_key=False, related_name="petition_patient")
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT,primary_key=False, related_name="petition_doctor")

    def __str__(self):
        return self.title
