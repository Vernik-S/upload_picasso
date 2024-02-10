from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet

from app.upload_file.serializers import FileSerializer


# Create your views here.
class UploadViewSet(GenericViewSet):
    """
    Class for uploading files
    """
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)

        

        return Response(serializer.data, status=status.HTTP_201_CREATED)