from celery import shared_task
from app.celery_settings import app

from upload_file.models import File


@shared_task()
#@app.task
def process_file(file_id):
    file = File.objects.get(id=file_id)
    file.processed = True
    print(file)
    file.save()