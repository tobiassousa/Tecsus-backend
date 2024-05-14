from django.urls import path
from agua.views import InserirDadosAPIView

urlpatterns = [
    path('upload/', InserirDadosAPIView.as_view(), name='upload_csv'),
]

