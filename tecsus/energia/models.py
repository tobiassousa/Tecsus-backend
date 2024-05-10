from django.db import models

class ContratoEnergia(models.Model):
    id_contrato_energia = models.AutoField(primary_key=True)
    fornecedor = models.CharField(max_length=10000)
    num_instalacao = models.CharField(max_length=10000)
    num_medidor = models.CharField(max_length=10000)
    num_cliente = models.CharField(max_length=10000)
    modalidade = models.CharField(max_length=10000)
    forma_pagto = models.CharField(max_length=10000)
    email_energia = models.CharField(max_length=10000)
    cidade = models.CharField(max_length=10000)
    num_contrato = models.CharField(max_length=10000)
    hor_ponta = models.CharField(max_length=1000)
    dem_ponta = models.CharField(max_length=1000)
    dem_fora_ponta = models.CharField(max_length=1000)
    data_extra = models.JSONField()

class ProEnergia(models.Model):
    id_pro_energia = models.AutoField(primary_key=True)
    leitura_anterior = models.CharField(max_length=10000)
    leitura_atual = models.CharField(max_length=10000)
    demanda_faturada_kw = models.CharField(max_length=10000)
    total = models.CharField(max_length=10000)
    fornecedor = models.CharField(max_length=10000)
    num_instalacao = models.CharField(max_length=10000)
    num_cliente = models.CharField(max_length=10000)
    modalidade = models.CharField(max_length=10000)
    num_contrato = models.CharField(max_length=10000)
    ben_tar_bruto = models.CharField(max_length=10000)
    ben_tar_liq = models.CharField(max_length=10000)
    con_pt_vd = models.CharField(max_length=1000, default='')
    con_fp_cad = models.CharField(max_length=1000,  default='')
    con_fp_ind = models.CharField(max_length=1000, default='')
    dem_fp_cad = models.CharField(max_length=1000, default='' )
    dem_pt = models.CharField(max_length=1000, default='' )
    dem_fp_ind = models.CharField(max_length=1000, default='' )
    grupos = models.CharField(max_length=1000, default='' )
    data_extra = models.JSONField()
    