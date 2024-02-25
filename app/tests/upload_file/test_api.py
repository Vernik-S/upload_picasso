import filecmp
import os
import random
import string
from io import BytesIO, StringIO
from time import sleep

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
from model_bakery import baker

from upload_file.models import File
from upload_file.tasks import process_file
from django.core.files import File as Fl
from django.contrib.staticfiles import finders


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def files_factory():
    def factory(*args, **kwargs):
        return baker.make(File, _create_files=True, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_list_files(client, files_factory):
    # Arrange
    files_test = files_factory(_quantity=10)

    # Act
    response = client.get(f'/api/v1/files/', follow=True)

    # Assert

    assert response.status_code == 200
    data = response.json()

    assert len(data) == len(files_test)

    for i, response_file in enumerate(data):
        assert response_file['file'].split('/')[-1] == files_test[i].file
        assert response_file['processed'] is False


@pytest.mark.celery(result_backend='redis://localhost:6379')
@pytest.mark.django_db
def test_processing_file(client):
    # Arrange
    random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(100))
    upload_file = SimpleUploadedFile('testfile.txt', random_string.encode())
    response = client.post(f'/api/v1/upload/', {'file': upload_file}, follow=True, )
    file_id = response.data["id"]
    print(file_id)

    # Act
    process_file.delay(file_id, content_type='text/plain')

    # Assert

    sleep(2) #waiting for celery result

    file_url = response.data['file']
    file_response = client.get(file_url)

    file_content = "".join([chunk.decode() for chunk in file_response])

    assert random_string.encode() != file_content.encode()
