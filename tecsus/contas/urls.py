from django.urls import path
from .views import UploadCSVView

urlpatterns = [
    path('upload/<str:model>/<str:documento>/', UploadCSVView.as_view(), name='upload_csv'),
]

