from celery import shared_task
from app.celery_settings import app

from PIL import Image
import PIL.ImageOps

from upload_file.models import File



@shared_task()
#@app.task
def process_file(file_id, content_type = None):
    file = File.objects.get(id=file_id)
    if content_type in ['image/jpeg', 'image/tiff']:
        file_name = file.file.path
        print(file_name)
        image = Image.open(file_name)
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save(file_name)



    file.processed = True
    file.save()