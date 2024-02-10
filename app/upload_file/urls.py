from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views  import UploadViewSet

app_name = 'upload_file'

r = DefaultRouter()
r.register("upload", UploadViewSet, basename="products")

urlpatterns = [
    path('', include(r.urls)),
]