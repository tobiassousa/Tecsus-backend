from django.db import models


class FornecedorEnergia(models.Model):
    id_fornecedor_energia = models.AutoField(primary_key=True)
    fornecedor = models.CharField(max_length=255)
    num_contrato = models.BigIntegerField(null=True)


class EnderecoEnergia(models.Model):
    id_endereco = models.AutoField(primary_key=True)
    endereco_instalacao = models.CharField(max_length=255)
    num_contrato = models.BigIntegerField(null=True)


class FatoContratoEnergia(models.Model):
    id_contrato_energia = models.AutoField(primary_key=True)
    fic_apurado = models.CharField(max_length=255)
    conta_mes = models.CharField(max_length=255)
    demanda_faturada = models.CharField(max_length=255)
    demanda_ultrapassada = models.CharField(max_length=255)
    consumo_pt_vd = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    consumo_fp_cap_vd = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    consumo_fp_ind_vd = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    taxa_rev_fatura = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    tarifas = models.CharField(max_length=255)
    num_contrato = models.CharField(max_length=255, null=True)
    grupo = models.CharField(max_length=255)
    tipo_consumidor = models.CharField(max_length=255)
    num_instalacao = models.CharField(max_length=255, null=True)
    num_medidor = models.CharField(max_length=255)
    leitura_anterior = models.DateField(null=True)
    leitura_atual = models.DateField(null=True)
    icms = models.CharField(max_length=255)
    dmics = models.CharField(max_length=255)
    dicris = models.CharField(max_length=255)
    dics = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    planta = models.CharField(max_length=255, null=True)
    modalidade = models.CharField(max_length=255, null=True)


class ClienteContrato(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome_contrato = models.CharField(max_length=255)
    email = models.EmailField()
    ativo = models.CharField(max_length=255)
    num_contrato = models.BigIntegerField(null=True)
    num_cliente = models.CharField(max_length=255, null=True)
    grupo = models.CharField(max_length=255)
    forma_pagamento = models.CharField(max_length=255, null=True)
    planta = models.CharField(max_length=255, null=True)
