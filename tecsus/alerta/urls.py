from django.urls import path
from . import views

urlpatterns = [
    path('alerta_energia/', views.AlertaEnergiaAPIVIew.as_view(), name='gerar_alerta'),
    path('alertas_agua/', views.AlertaAguaAPIView.as_view(), name='listar_alertas'),
    # path('obter/<int:alert_id>/', views.obter_alerta_por_id, name='obter_alerta_por_id'),
]