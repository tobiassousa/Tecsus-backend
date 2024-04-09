from django.urls import path
from .views import UploadCSVView, AguaListView

urlpatterns = [
    path('agua/', AguaListView.as_view(), name='agua_list'),
    path('upload/<str:model>/<str:documento>/', UploadCSVView.as_view(), name='upload_csv'),
]


