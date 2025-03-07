from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name
