from django.db import models


class FornecedorAgua(models.Model):
    id_fornecedor_agua = models.AutoField(primary_key=True)
    fornecedor = models.CharField(max_length=255)
    cod_companhia = models.IntegerField()
    planta = models.CharField(max_length=255)
    codigo_de_ligacao_rgi = models.CharField(max_length=255, unique=True)


class Endereco(models.Model):
    id_endereco = models.AutoField(primary_key=True)
    endereco_instalacao = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)


class FatoContratoAgua(models.Model):
    id_contrato_agua = models.AutoField(primary_key=True)
    codigo_de_ligacao_rgi = models.IntegerField()
    id_endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    consumo_agua_m3 = models.IntegerField()
    consumo_esgoto_m3 = models.IntegerField()
    vlr_agua = models.DecimalField(max_digits=10, decimal_places=2)
    vlr_esgoto = models.DecimalField(max_digits=10, decimal_places=2)
    vlr_total = models.DecimalField(max_digits=10, decimal_places=2)
    leitura_anterior = models.DateField()
    leitura_atual = models.DateField()
