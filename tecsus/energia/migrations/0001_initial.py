# Generated by Django 5.0.6 on 2024-05-29 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteContrato',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nome_contrato', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('ativo', models.CharField(max_length=255)),
                ('num_contrato', models.BigIntegerField(null=True)),
                ('num_cliente', models.CharField(max_length=255, null=True)),
                ('num_instalacao', models.CharField(max_length=255, null=True)),
                ('grupo', models.CharField(max_length=255)),
                ('forma_pagamento', models.CharField(max_length=255, null=True)),
                ('planta', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnderecoEnergia',
            fields=[
                ('id_endereco', models.AutoField(primary_key=True, serialize=False)),
                ('endereco_instalacao', models.CharField(max_length=255)),
                ('num_contrato', models.BigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FatoContratoEnergia',
            fields=[
                ('id_contrato_energia', models.AutoField(primary_key=True, serialize=False)),
                ('fic_apurado', models.CharField(max_length=255)),
                ('conta_mes', models.CharField(max_length=255)),
                ('demanda_faturada', models.CharField(max_length=255)),
                ('demanda_ultrapassada', models.CharField(max_length=255)),
                ('demanda_pt', models.CharField(max_length=255, null=True)),
                ('demanda_fp_cap', models.CharField(max_length=255, null=True)),
                ('demanda_fp_ind', models.CharField(max_length=255, null=True)),
                ('consumo_pt_vd', models.DecimalField(decimal_places=2, max_digits=1000, null=True)),
                ('consumo_fp_cap_vd', models.DecimalField(decimal_places=2, max_digits=1000, null=True)),
                ('consumo_fp_ind_vd', models.DecimalField(decimal_places=2, max_digits=1000, null=True)),
                ('taxa_rev_fatura', models.DecimalField(decimal_places=2, max_digits=1000, null=True)),
                ('tarifas', models.CharField(max_length=255)),
                ('num_contrato', models.CharField(max_length=255, null=True)),
                ('grupo', models.CharField(max_length=255)),
                ('tipo_consumidor', models.CharField(max_length=255)),
                ('num_instalacao', models.CharField(max_length=255, null=True)),
                ('num_medidor', models.CharField(max_length=255)),
                ('leitura_anterior', models.DateField(null=True)),
                ('leitura_atual', models.DateField(null=True)),
                ('icms', models.CharField(max_length=255)),
                ('dmics', models.CharField(max_length=255)),
                ('dicris', models.CharField(max_length=255)),
                ('dics', models.CharField(max_length=255)),
                ('total', models.DecimalField(decimal_places=2, max_digits=1000, null=True)),
                ('planta', models.CharField(max_length=255, null=True)),
                ('modalidade', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FornecedorEnergia',
            fields=[
                ('id_fornecedor_energia', models.AutoField(primary_key=True, serialize=False)),
                ('fornecedor', models.CharField(max_length=255)),
                ('num_contrato', models.BigIntegerField(null=True)),
            ],
        ),
    ]
