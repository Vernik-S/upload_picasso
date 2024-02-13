from django.db import models
from django.db.models import FileField, Model, DateTimeField, BooleanField

from .validators import FileValidator


# Create your models here.
class File(Model):
    validate_file = FileValidator(max_size=1024 * 1024 * 1,  # 1 Mb
                                  # content_types='application/xml',
                                  )
    file = FileField(validators=[validate_file])
    created_at = DateTimeField(auto_now_add=True, verbose_name="When was this file uploaded")
    processed = BooleanField(verbose_name='file processed status', default=False)
