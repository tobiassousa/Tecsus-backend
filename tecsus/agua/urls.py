from django.urls import path
from .views import ContratoAguaAPIView, ProAguaAPIView, consulta_contrato_pro_agua

urlpatterns = [
    path('contrato_agua/', ContratoAguaAPIView.as_view(), name='contrato_agua_api'),
    path('pro_agua/', ProAguaAPIView.as_view(), name='pro_agua_api'),
    path('query_agua/', consulta_contrato_pro_agua, name='pro_con'),
]
