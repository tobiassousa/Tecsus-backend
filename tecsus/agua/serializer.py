from rest_framework import serializers
<<<<<<< HEAD:tecsus/agua/serializer.py

from .models import AlertaAgua
=======
from .models import AlertaAgua, AlertaEnergia
>>>>>>> dev:tecsus/alerta/serializer.py

class AlertaAguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertaAgua
<<<<<<< HEAD:tecsus/agua/serializer.py
        fields = ['id_alerta', 'id_user_alerta', 'alert_user_email', 'alert_consumo_media', 'alert_consumo_atual', 'alert_conta']
=======
        fields = ['id_alerta', 'id_user_alerta', 'alert_user_email', 'alert_consumo_media', 'alert_consumo_atual', 'alert_conta']


class AlertaEnergiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertaEnergia
        fields = ['id_alerta', 'id_user_alerta', 'alert_user_email', 'alert_consumo_media', 'alert_consumo_atual', 'alert_conta']
>>>>>>> dev:tecsus/alerta/serializer.py
