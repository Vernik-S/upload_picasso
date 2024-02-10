from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet

from .models import File
from .serializers import FileSerializer
from .tasks import process_file

# Create your views here.
class UploadViewSet(GenericViewSet):
    """
    Class for uploading files
    """
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.save()
        file.save()
        process_file.delay(file.id)


        return Response(serializer.data, status=status.HTTP_201_CREATED)