from django.urls import path
from .views import AlertaEnergiaAPIView, ContratoEnergiaAPIView, ProEnergiaAPIView, consulta_contrato_pro_energia

urlpatterns = [
    path('contrato_energia/', ContratoEnergiaAPIView.as_view(), name='contrato_energia_api'),
    path('pro_energia/', ProEnergiaAPIView.as_view(), name='pro_energia_api'),
    path('alertas_energia/', AlertaEnergiaAPIView.as_view(), name='alerta_energia_api'),
    path('query_energia/', consulta_contrato_pro_energia, name='query_energia'),
]
