import pytest

from rest_framework.test import APIClient
from model_bakery import baker

from upload_file.models import File


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
