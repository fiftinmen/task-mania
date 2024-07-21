from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name


"""     def delete(self, *args, **kwargs):
        if self.tasks.exists():
            raise ValidationError(
                _(
                    "Cannot delete this label because it is associated with"
                    "one or more tasks."
                )
            )
        super().delete(*args, **kwargs)
 """
