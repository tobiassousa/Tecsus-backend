from rest_framework import serializers

from .models import AlertaEnergia

class AlertaEnergiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertaEnergia
        fields = ['id_alerta', 'id_user_alerta', 'alert_user_email', 'alert_consumo_media', 'alert_consumo_atual', 'alert_conta']