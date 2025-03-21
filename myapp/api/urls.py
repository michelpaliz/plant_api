from django.urls import path
from myapp.api.views import test_upload_simple, predict_image

urlpatterns = [
    path("test-upload-simple/", test_upload_simple, name="test_upload_simple"),
    path("predict/", predict_image, name="predict_image"),
]
