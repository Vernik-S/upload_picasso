from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views  import UploadViewSet

app_name = 'upload_file'

r = DefaultRouter()
r.register("", UploadViewSet)

urlpatterns = [
    path('', include(r.urls)),
]