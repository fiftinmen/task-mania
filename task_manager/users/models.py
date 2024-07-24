from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

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
