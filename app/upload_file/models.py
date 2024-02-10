from django.db import models
from django.db.models import FileField, Model, DateTimeField, BooleanField


# Create your models here.
class File(Model):
    file = FileField()
    created_at = DateTimeField(auto_now_add=True, verbose_name="When was this file uploaded")
    processed = BooleanField(verbose_name='file processed status', default=False)
