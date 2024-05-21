import csv
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FornecedorEnergia, EnderecoEnergia, FatoContratoEnergia, ClienteContrato
from datetime import datetime
from django.core.files.storage import default_storage
from rest_framework import generics
from .serializers import FornecedorEnergiaSerializer, FatoContratoEnergiaSerializer, ClienteContratoSerializer
# from .utils import comparar_media_mes_atual_com_ultimos_tres_meses


class FornecedorEnergiaAPIView(generics.ListAPIView):
    queryset = FornecedorEnergia.objects.all()
    serializer_class = FornecedorEnergiaSerializer


class EnderecoEnergiaAPIView(generics.ListAPIView):
    queryset = FornecedorEnergia.objects.all()
    serializer_class = FornecedorEnergiaSerializer


class FatoContratoEnergiaAPIView(generics.ListAPIView):
    queryset = FatoContratoEnergia.objects.all()
    serializer_class = FatoContratoEnergiaSerializer


class ClienteContratoAPIView(generics.ListAPIView):
    queryset = ClienteContrato.objects.all()
    serializer_class = ClienteContratoSerializer


class InserirDadosAPIView(APIView):
    def post(self, request):
        tipo_documento = request.data.get('tipo_documento')
        arquivo_csv = request.FILES.get('arquivo_csv')

        if not tipo_documento or not arquivo_csv:
            return Response({'error': 'Tipo de documento e arquivo CSV são necessários.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pasta_csv = 'csv_upload/energia'
            caminho_csv = os.path.join(pasta_csv, arquivo_csv.name)
            caminho_relatorio = default_storage.save(caminho_csv, arquivo_csv)  
            if tipo_documento == 'contrato':
                self.inserir_contratos_do_csv(caminho_csv)
            elif tipo_documento == 'fatura':
                self.inserir_faturas_do_csv(caminho_csv)
            else:
                return Response({'error': 'Tipo de documento inválido.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': f'Dados do {tipo_documento} inseridos com sucesso.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def inserir_contratos_do_csv(self, caminho_do_csv):
        with default_storage.open(caminho_do_csv, 'r') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            for linha in leitor_csv:
                num_cliente = linha['Número Cliente'] or None
                num_contrato = linha['Número Contrato']
                if not num_contrato.isdigit():
                    num_contrato = None

                if ClienteContrato.objects.filter(num_contrato=num_contrato).exists():
                    continue

                fornecedor_energia, _ = FornecedorEnergia.objects.get_or_create(
                    fornecedor=linha['Fornecedor'],
                    num_contrato=num_contrato,
                )

                endereco_energia, _ = EnderecoEnergia.objects.get_or_create(
                    endereco_instalacao=linha['Endereço de Instalação'],
                    num_contrato=num_contrato,
                )

                contrato, _ = ClienteContrato.objects.get_or_create(
                    nome_contrato=linha['Nome do Contrato'],
                    email=linha['Campo Extra de Acesso 1'],
                    ativo=linha['Ativado'],
                    num_contrato=num_contrato,
                    num_cliente=num_cliente,
                    planta = linha['Planta'],
                    forma_pagamento = linha['Forma de Pagamento']
                )

    def inserir_faturas_do_csv(self, caminho_do_csv):
        with default_storage.open(caminho_do_csv, 'r') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            for linha in leitor_csv:
                num_contrato = linha['Número Contrato']

                leitura_anterior = self.converter_para_data(linha['Leitura Anterior'])
                leitura_atual = self.converter_para_data(linha['Leitura Atual'])

                consumo_pt_vd = self.converter_para_decimal(linha['Consumo PT VD'])
                consumo_fp_cap_vd = self.converter_para_decimal(linha['Consumo FP CAP VD'])
                consumo_fp_ind_vd = self.converter_para_decimal(linha['Consumo FP IND VD'])
                taxa_rev_fatura = self.converter_para_decimal(linha['Taxa Revisão de Fatura'])

                total = self.converter_para_decimal(linha['Total'])

                fic_apurado = linha['FIC Apurado']
                conta_mes = linha['Conta do Mês']
                demanda_faturada = linha['Demanda Faturada (kW)']
                demanda_ultrapassada = linha['Demanda Ultrapassada (kW)']
                consumo_pt_vd = consumo_pt_vd
                consumo_fp_cap_vd = consumo_fp_cap_vd
                consumo_fp_ind_vd = consumo_fp_ind_vd
                taxa_rev_fatura = taxa_rev_fatura
                tarifas = linha['Tarifa Energia Reativa PT C/ Imposto']
                grupo = linha['grupo']
                tipo_consumidor = linha['Código de Consumidor']
                num_instalacao = linha['Número Instalação']
                num_medidor = linha['Número Medidor']
                leitura_atual = leitura_atual
                leitura_anterior = leitura_anterior
                icms = linha['ICMS']
                dmics = linha['DMIC']
                dicris = linha['DICRI']
                dics = linha['DIC']
                total = total
                planta = linha['Planta']
                modalidade = linha['Modalidade']

                FatoContratoEnergia.objects.create(
                    fic_apurado=fic_apurado,
                    conta_mes=conta_mes,
                    demanda_faturada=demanda_faturada,
                    demanda_ultrapassada=demanda_ultrapassada,
                    consumo_pt_vd=consumo_pt_vd,
                    consumo_fp_cap_vd=consumo_fp_cap_vd,
                    consumo_fp_ind_vd=consumo_fp_ind_vd,
                    taxa_rev_fatura=taxa_rev_fatura,
                    tarifas=tarifas,
                    num_contrato=num_contrato,
                    grupo=grupo,
                    tipo_consumidor=tipo_consumidor,
                    num_instalacao=num_instalacao,
                    num_medidor=num_medidor,
                    leitura_atual=leitura_atual,
                    leitura_anterior=leitura_anterior,
                    icms=icms,
                    dmics=dmics,
                    dicris=dicris,
                    dics=dics,
                    total = total,
                    modalidade = modalidade,
                    planta = planta,
                )

    def converter_para_decimal(self, valor_str):
        valor_str = valor_str.strip().replace('.', '').replace(',', '.')
        return float(valor_str)

    def converter_para_data(self, data_str):
        try:
            if data_str == '00/00/0000':
                return None
            else:
                return datetime.strptime(data_str, '%d/%m/%Y')
        except ValueError:
            return None