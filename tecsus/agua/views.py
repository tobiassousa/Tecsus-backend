from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FornecedorAgua, Endereco, ClienteContrato, FatoContratoAgua
import csv
from datetime import datetime
from django.core.files.storage import default_storage


class InserirDadosAPIView(APIView):
    def post(self, request):
        tipo_documento = request.data.get('tipo_documento')
        arquivo_csv = request.FILES.get('arquivo_csv')

        if not tipo_documento or not arquivo_csv:
            return Response({'error': 'Tipo de documento e arquivo CSV são necessários.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            caminho_csv = default_storage.save(arquivo_csv.name, arquivo_csv)
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
                numero_cliente = linha['Número Cliente'] or None
                
                numero_contrato = linha['Número Contrato']
                if not numero_contrato.isdigit():
                    numero_contrato = None

                codigo_de_ligacao_rgi = linha['Código de Ligação (RGI)']
                if ClienteContrato.objects.filter(codigo_de_ligacao_rgi=codigo_de_ligacao_rgi).exists():
                    continue

                fornecedor_agua, _ = FornecedorAgua.objects.get_or_create(
                    fornecedor=linha['Fornecedor'],
                    cod_companhia=linha['Codificação da Companhia'],
                    planta=linha['Planta'],
                    codigo_de_ligacao_rgi=codigo_de_ligacao_rgi
                )

                endereco, _ = Endereco.objects.get_or_create(
                    endereco_instalacao=linha['Endereço de Instalação'],
                    cidade=linha['Nome do Contrato']
                )

                contrato, _ = ClienteContrato.objects.get_or_create(
                    nome_contrato=linha['Nome do Contrato'],
                    email=linha['Campo Extra de Acesso 1'],
                    ativo=linha['Ativado'],
                    numero_contrato=numero_contrato,
                    numero_cliente=numero_cliente,
                    codigo_de_ligacao_rgi=codigo_de_ligacao_rgi
                )

    def inserir_faturas_do_csv(self, caminho_do_csv):
        with default_storage.open(caminho_do_csv, 'r') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            for linha in leitor_csv:
                contrato = ClienteContrato.objects.get(codigo_de_ligacao_rgi=linha['Código de Ligação (RGI)'])

                endereco_instalacao = linha.get('Endereço de Instalação', 'Endereço desconhecido')

                cidade = linha.get('Cidade', '')

                endereco, _ = Endereco.objects.get_or_create(
                    endereco_instalacao=endereco_instalacao,
                    cidade=cidade
                )

                consumo_agua_m3 = self.converter_para_decimal(linha['Consumo de Água m³'])
                consumo_esgoto_m3 = self.converter_para_decimal(linha['Consumo de Esgoto m³'])
                vlr_agua = self.converter_para_decimal(linha['Valor Água R$'])
                vlr_esgoto = self.converter_para_decimal(linha['Valor Esgoto R$'])
                vlr_total = self.converter_para_decimal(linha['Total R$'])

                leitura_anterior = self.converter_para_data(linha['Leitura Anterior'])
                leitura_atual = self.converter_para_data(linha['Leitura Atual'])

                FatoContratoAgua.objects.create(
                    codigo_de_ligacao_rgi=contrato,
                    id_endereco=endereco,
                    consumo_agua_m3=consumo_agua_m3,
                    consumo_esgoto_m3=consumo_esgoto_m3,
                    vlr_agua=vlr_agua,
                    vlr_esgoto=vlr_esgoto,
                    vlr_total=vlr_total,
                    leitura_anterior=leitura_anterior,
                    leitura_atual=leitura_atual,
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