from random import choice

from celery import shared_task
from app.celery_settings import app

from PIL import Image
import PIL.ImageOps

from upload_file.models import File



@shared_task()
#@app.task
def process_file(file_id, content_type = None):
    file = File.objects.get(id=file_id)
    file_name = file.file.path
    if content_type in ['image/jpeg', 'image/tiff']:
        image = Image.open(file_name)
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save(file_name)
    elif content_type in ['text/plain']:
        new_lines = []
        with open(file_name, "r") as f:
            for line in f:
                randomized_line = ''.join(choice((str.upper, str.lower))(char) for char in line)
                print(randomized_line)
                new_lines.append(randomized_line)
        with open(file_name, "w") as f:
            f.writelines(new_lines)




    file.processed = True
    file.save()