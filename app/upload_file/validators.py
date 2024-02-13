import magic

from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from rest_framework.exceptions import ValidationError

# from https://stackoverflow.com/questions/20272579/django-validate-file-type-of-uploaded-file
@deconstructible
class FileValidator(object):

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(detail=[f"Ensure this file size is not greater than {params['max_size']}",
                                          f"Your file size is {params['size']}"]
                                  )

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(detail=[f"Ensure this file size is not less than {params['min_size']}",
                                          f"Your file size is {params['size']}"]
                                  )

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                raise ValidationError(detail=f"{content_type} type is not supported")

    def __eq__(self, other):
        return (
                isinstance(other, FileValidator) and
                self.max_size == other.max_size and
                self.min_size == other.min_size and
                self.content_types == other.content_types
        )
