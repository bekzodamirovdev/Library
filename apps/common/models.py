from django.db import models


DEGREE = (
    ("1", 'bachelor'),
    ("2", 'master'),
    ("3", 'doctor')
)


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


