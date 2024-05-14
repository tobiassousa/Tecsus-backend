from django.db import models


class FornecedorAgua(models.Model):
    id_fornecedor_agua = models.AutoField(primary_key=True)
    fornecedor = models.CharField(max_length=255)
    cod_companhia = models.CharField(max_length=255)
    planta = models.CharField(max_length=255)
    codigo_de_ligacao_rgi = models.CharField(max_length=255, unique=True)


class Endereco(models.Model):
    id_endereco = models.AutoField(primary_key=True)
    endereco_instalacao = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)


class ClienteContrato(models.Model):
    nome_contrato = models.CharField(max_length=255, null=True)
    email = models.EmailField()
    ativo = models.CharField(max_length=255)
    numero_contrato = models.BigIntegerField(null=True)
    numero_cliente = models.BigIntegerField(null=True)
    codigo_de_ligacao_rgi = models.CharField(max_length=255, primary_key=True)


class FatoContratoAgua(models.Model):
    id_contrato_agua = models.AutoField(primary_key=True)
    codigo_de_ligacao_rgi = models.ForeignKey(ClienteContrato, on_delete=models.CASCADE)
    id_endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    consumo_agua_m3 = models.DecimalField(max_digits=1000, decimal_places=2)
    consumo_esgoto_m3 = models.DecimalField(max_digits=1000, decimal_places=2)
    vlr_agua = models.DecimalField(max_digits=1000, decimal_places=2)
    vlr_esgoto = models.DecimalField(max_digits=1000, decimal_places=2)
    vlr_total = models.DecimalField(max_digits=1000, decimal_places=2)
    leitura_anterior = models.DateField(null=True)
    leitura_atual = models.DateField(null=True)
