from rest_framework import serializers

from app.upload_file.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'created_at', 'processed']