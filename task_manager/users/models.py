from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create(
        self,
        username,
        first_name,
        last_name,
        date_joined,
        email=None,
        password=None,
    ):
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_joined=date_joined,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        email,
        date_joined,
        first_name=None,
        last_name=None,
        password=None,
    ):
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_joined=date_joined,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    class Meta:
        permissions = [
            ("users.update_all", "Can update all users"),
            ("users.delete_all", "Can delete all users"),
            ("users.update_self", "Can self update"),
            ("users.delete_self", "Can self delete"),
        ]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username
