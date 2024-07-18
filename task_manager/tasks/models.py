from django.db import models
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=100, default="name", unique=True)
    description = models.TextField(max_length=2048, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="task_author",
    )
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="task_executor",
        blank=True,
        null=True,
    )
    REQUIRED_FIELDS = ["name", "status", "author"]
