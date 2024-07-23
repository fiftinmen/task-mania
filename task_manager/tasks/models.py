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
    labels = models.ManyToManyField(
        to="labels.Label", through="TaskLabels", blank=True
    )

    REQUIRED_FIELDS = ["name", "status", "author"]

    class Meta:
        permissions = [
            ("tasks.delete_all", "Can delete all tasks"),
            ("tasks.delete_own", "Can delete own tasks"),
        ]

    def __str__(self):
        return self.name


class TaskLabels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(to="labels.Label", on_delete=models.PROTECT)
