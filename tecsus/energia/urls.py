from django.urls import path

from .views import ContratoEnergiaAPIView, ProEnergiaAPIView, consulta_contrato_pro_energia, MediaConsumoUltimosTresMesesAPIView

urlpatterns = [
    path('contrato_energia/', ContratoEnergiaAPIView.as_view(), name='contrato_energia_api'),
    path('pro_energia/', ProEnergiaAPIView.as_view(), name='pro_energia_api'),
    path('query_energia/', consulta_contrato_pro_energia, name='query_energia'),
    path('media_consumo/<str:num_cliente>/', MediaConsumoUltimosTresMesesAPIView.as_view(), name='media_consumo_tres_meses'),
]
