import csv
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FornecedorAgua, Endereco, ClienteContrato, FatoContratoAgua
from datetime import datetime
from django.core.files.storage import default_storage
from rest_framework import generics
from .serializers import FornecedorAguaSerializer, EnderecoSerializer, ClienteContratoSerializer, FatoContratoAguaSerializer
from .utils import comparar_media_mes_atual_com_ultimos_tres_meses
from django.db.models import Case, When, Value, BooleanField
from django.db import connection


class FornecedorAguaAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        id_fornecedor_agua = self.kwargs.get('id_fornecedor_agua')
        
        if id_fornecedor_agua is not None:
            try:
                fornecedor = FornecedorAgua.objects.get(id_fornecedor_agua=id_fornecedor_agua)
                serializer = FornecedorAguaSerializer(fornecedor)
                return Response(serializer.data)
            except FornecedorAgua.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            fornecedores = FornecedorAgua.objects.order_by('fornecedor').distinct('fornecedor')
            serializer = FornecedorAguaSerializer(fornecedores, many=True)
            return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = FornecedorAguaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        id_fornecedor_agua = self.kwargs.get('id_fornecedor_agua')
        
        if id_fornecedor_agua is not None:
            try:
                fornecedor = FornecedorAgua.objects.get(id_fornecedor_agua=id_fornecedor_agua)
                serializer = FornecedorAguaSerializer(fornecedor, data=request.data, partial=True)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except FornecedorAgua.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "ID do fornecedor de água não fornecido."}, status=status.HTTP_400_BAD_REQUEST)


class EnderecoAPIView(generics.ListAPIView):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer



class ClienteContratoAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        codigo_de_ligacao_rgi = self.kwargs.get('codigo_de_ligacao_rgi')
        
        if codigo_de_ligacao_rgi is not None:
            try:
                cliente = ClienteContrato.objects.get(codigo_de_ligacao_rgi=codigo_de_ligacao_rgi)
                serializer = ClienteContratoSerializer(cliente)
                return Response(serializer.data)
            except ClienteContrato.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            clientes = ClienteContrato.objects.annotate(
                has_contrato=Case(
                    When(numero_contrato__isnull=True, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ).order_by('has_contrato')
            serializer = ClienteContratoSerializer(clientes, many=True)
            return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ClienteContratoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        codigo_de_ligacao_rgi = self.kwargs.get('codigo_de_ligacao_rgi')
        
        if codigo_de_ligacao_rgi is not None:
            try:
                cliente = ClienteContrato.objects.get(codigo_de_ligacao_rgi=codigo_de_ligacao_rgi)
                serializer = ClienteContratoSerializer(cliente, data=request.data, partial=True)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except ClienteContrato.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "ID do cliente não fornecido."}, status=status.HTTP_400_BAD_REQUEST)


class FatoContratoAguaList(APIView):
    def get(self, request, format=None):
        contratos = FatoContratoAgua.objects.all()
        serializer = FatoContratoAguaSerializer(contratos, many=True)
        return Response(serializer.data)


class AllDataAPIView(APIView):
    def get(self, request, format=None):
        fornecedores = FornecedorAgua.objects.all()
        enderecos = Endereco.objects.all()
        contratos = ClienteContrato.objects.all()
        fatos_contratos = FatoContratoAgua.objects.all()

        fornecedores_data = FornecedorAguaSerializer(fornecedores, many=True).data
        enderecos_data = EnderecoSerializer(enderecos, many=True).data
        contratos_data = ClienteContratoSerializer(contratos, many=True).data
        fatos_contratos_data = FatoContratoAguaSerializer(fatos_contratos, many=True).data

        return Response({
            'fornecedores': fornecedores_data,
            'enderecos': enderecos_data,
            'contratos': contratos_data,
            'fatos_contratos': fatos_contratos_data,
        })


class InserirDadosAPIView(APIView):
    def post(self, request):
        tipo_documento = request.data.get('tipo_documento')
        arquivo_csv = request.FILES.get('arquivo_csv')

        if not tipo_documento or not arquivo_csv:
            return Response({'error': 'Tipo de documento e arquivo CSV são necessários.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pasta_csv = 'csv_upload/agua'
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
                    cidade=linha['Nome do Contrato'],
                    codigo_de_ligacao_rgi=codigo_de_ligacao_rgi
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
        

class CompareMesAtualComTresUltimosMeses(APIView):
    def get(self, request, codigo_de_ligacao_rgi):
        try:
            comparison_result = comparar_media_mes_atual_com_ultimos_tres_meses(codigo_de_ligacao_rgi)
            return Response({"message": comparison_result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class AllDataAPIView(APIView):
    def get(self, request, format=None):
        fornecedores = FornecedorAgua.objects.all()
        enderecos = Endereco.objects.all()
        contratos = ClienteContrato.objects.all()
        fatos_contrato = FatoContratoAgua.objects.all()

        fornecedores_data = FornecedorAguaSerializer(fornecedores, many=True).data
        enderecos_data = EnderecoSerializer(enderecos, many=True).data
        contratos_data = ClienteContratoSerializer(contratos, many=True).data
        fatos_contrato_data = FatoContratoAguaSerializer(fatos_contrato, many=True).data

        combined_data = []
        for contrato in contratos_data:
            codigo_de_ligacao_rgi = contrato['codigo_de_ligacao_rgi']
            fatos_contrato_cliente = [fato for fato in fatos_contrato_data if fato['codigo_de_ligacao_rgi'] == codigo_de_ligacao_rgi]
            fornecedor_cliente = next((fornecedor for fornecedor in fornecedores_data if fornecedor['codigo_de_ligacao_rgi'] == codigo_de_ligacao_rgi), {})
            endereco_cliente = next((endereco for endereco in enderecos_data if endereco['codigo_de_ligacao_rgi'] == codigo_de_ligacao_rgi), {})

            for fato in fatos_contrato_cliente:
                combined_data.append({
                    'contrato_nome': contrato['nome_contrato'],
                    'contrato_email': contrato['email'],
                    'contrato_ativo': contrato['ativo'],
                    'contrato_numero_contrato': contrato['numero_contrato'],
                    'contrato_numero_cliente': contrato['numero_cliente'],
                    'contrato_codigo_de_ligacao_rgi': contrato['codigo_de_ligacao_rgi'],

                    'fato_id': fato['id_contrato_agua'],
                    'fato_consumo_agua_m3': fato['consumo_agua_m3'],
                    'fato_consumo_esgoto_m3': fato['consumo_esgoto_m3'],
                    'fato_vlr_agua': fato['vlr_agua'],
                    'fato_vlr_esgoto': fato['vlr_esgoto'],
                    'fato_vlr_total': fato['vlr_total'],
                    'fato_leitura_anterior': fato['leitura_anterior'],
                    'fato_leitura_atual': fato['leitura_atual'],

                    'endereco_id': endereco_cliente.get('id_endereco', None),
                    'endereco_instalacao': endereco_cliente.get('endereco_instalacao', None),
                    'endereco_cidade': endereco_cliente.get('cidade', None),

                    'fornecedor_id': fornecedor_cliente.get('id_fornecedor_agua', None),
                    'fornecedor_nome': fornecedor_cliente.get('fornecedor', None),
                    'fornecedor_cod_companhia': fornecedor_cliente.get('cod_companhia', None),
                    'fornecedor_planta': fornecedor_cliente.get('planta', None),
                    'fornecedor_codigo_de_ligacao_rgi': fornecedor_cliente.get('codigo_de_ligacao_rgi', None),
                })

        return Response(combined_data)