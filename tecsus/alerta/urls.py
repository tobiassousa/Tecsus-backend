from django.urls import path
from . import views

urlpatterns = [
    path('gerar/', views.AlertaAguaAPIView.as_view(), name='gerar_alerta'),
    path('listar/', views.AlertaAguaAPIView.as_view(), name='listar_alertas'),
    # path('obter/<int:alert_id>/', views.obter_alerta_por_id, name='obter_alerta_por_id'),
]