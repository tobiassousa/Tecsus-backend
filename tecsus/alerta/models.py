from django.db import models

class AlertaAgua(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    id_user_alerta = models.CharField(max_length=10000)
    alert_user_email = models.EmailField(max_length=1000)
    alert_consumo_media = models.CharField(max_length=1000)
    alert_consumo_atual = models.CharField(max_length=1000)
    alert_conta = models.CharField(max_length=10000)