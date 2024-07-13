from django.db import models
from task_manager.statuses.models import Status


# Create your models here.
class Task(models.Model):
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
