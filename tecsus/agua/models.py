from django.db import models

class ContratoAgua(models.Model):
    id_contrato_agua = models.AutoField(primary_key=True)
    fornecedor = models.CharField(max_length=10000)
    num_instalacao = models.CharField(max_length=10000)
    num_medidor = models.CharField(max_length=10000)
    num_cliente = models.CharField(max_length=10000)
    modalidade = models.CharField(max_length=10000)
    num_contrato = models.CharField(max_length=10000)
    tipo_pagto = models.CharField(max_length=10000)
    email_agua = models.CharField(max_length=10000)
    cidade = models.CharField(max_length=10000)
    cod_ligacao_rgi = models.CharField(max_length=10000)
    data_extra = models.JSONField()

class ProAgua(models.Model):
    id_pro_agua = models.AutoField(primary_key=True)
    leitura_anterior = models.CharField(max_length=10000)
    leitura_atual = models.CharField(max_length=10000)
    consumo_agua_m3 = models.CharField(max_length=10000)
    consumo_esgoto_m3 = models.CharField(max_length=10000)
    vlr_agua = models.CharField(max_length=10000)
    vlr_esgoto = models.CharField(max_length=10000)
    vlr_total = models.CharField(max_length=10000)
    num_instalacao = models.CharField(max_length=10000)
    num_medidor = models.CharField(max_length=10000)
    num_cliente = models.CharField(max_length=10000)
    cod_ligacao_rgi = models.CharField(max_length=10000)
    num_contrato = models.CharField(max_length=10000)
    data_extra = models.JSONField()
    

class AlertaAgua(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    id_user_alerta = models.CharField(max_length=10000)
    alert_user_email = models.EmailField(max_length=1000)
    alert_consumo_media = models.CharField(max_length=1000)
    alert_consumo_atual = models.CharField(max_length=1000)
    alert_conta = models.CharField(max_length=10000)
