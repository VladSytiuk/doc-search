from django.urls import path

from app.api.v1.views import SignUpUserView, UserListView, DocumentUploadAPIView

urlpatterns = [
    path("sign-up/", SignUpUserView.as_view(), name="sign-up"),
    path("users", UserListView.as_view(), name="users"),
    path("upload-document/", DocumentUploadAPIView.as_view(), name="upload-document"),
]
