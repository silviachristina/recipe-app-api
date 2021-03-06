# used to generate the uuid
import uuid
# used to create a valid path for our file destination
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

# Recomended way to retreive user auth
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    # Split the string and return the last part (the file extension)
    ext = filename.split('.')[-1]
    # creates a string with a randon uuid and the file extension
    filename = f'{uuid.uuid4()}.{ext}'
    # join the destination path we want store the file
    # help function that allows join two strings together to make a valid path
    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')

        # user = self.model(email=self.normalize_email(email), **extra_fields)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    # If you delete this user it will delete the tag as well
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # String representation of the model

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe objects"""
    # One to many - Many users to one recipe
    # Each recipe can have one be assign to one user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # Optional fields
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    # Optional, pass the function to upload_to, pass the reference
    # Call everytime we upload, will be called in the background by django
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
