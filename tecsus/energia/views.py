import csv
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FornecedorEnergia, EnderecoEnergia, FatoContratoEnergia, ClienteContrato
from datetime import datetime
from django.core.files.storage import default_storage
from rest_framework import generics
from .serializers import FornecedorEnergiaSerializer, FatoContratoEnergiaSerializer, ClienteContratoSerializer, EnderecoSerializer
# from .utils import comparar_media_mes_atual_com_ultimos_tres_meses


class FornecedorEnergiaAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        id_fornecedor_energia = self.kwargs.get('id_fornecedor_energia')
        
        if id_fornecedor_energia is not None:
            try:
                fornecedor = FornecedorEnergia.objects.get(id_fornecedor_energia=id_fornecedor_energia)
                serializer = FornecedorEnergiaSerializer(fornecedor)
                return Response(serializer.data)
            except FornecedorEnergia.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            fornecedores = FornecedorEnergia.objects.all()
            serializer = FornecedorEnergiaSerializer(fornecedores, many=True)
            return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = FornecedorEnergiaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        id_fornecedor_energia = self.kwargs.get('id_fornecedor_energia')
        
        if id_fornecedor_energia is not None:
            try:
                fornecedor = FornecedorEnergia.objects.get(id_fornecedor_energia=id_fornecedor_energia)
                serializer = FornecedorEnergiaSerializer(fornecedor, data=request.data, partial=True)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except FornecedorEnergia.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "ID do fornecedor de água não fornecido."}, status=status.HTTP_400_BAD_REQUEST)
    


class EnderecoEnergiaAPIView(generics.ListAPIView):
    queryset = FornecedorEnergia.objects.all()
    serializer_class = FornecedorEnergiaSerializer


class FatoContratoEnergiaAPIView(generics.ListAPIView):
    queryset = FatoContratoEnergia.objects.all()
    serializer_class = FatoContratoEnergiaSerializer


class ClienteContratoAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        id_cliente = self.kwargs.get('id_cliente')
        
        if id_cliente is not None:
            try:
                cliente = ClienteContrato.objects.get(id_cliente=id_cliente)
                serializer = ClienteContratoSerializer(cliente)
                return Response(serializer.data)
            except ClienteContrato.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            clientes = ClienteContrato.objects.all()
            serializer = ClienteContratoSerializer(clientes, many=True)
            return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ClienteContratoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        id_cliente = self.kwargs.get('id_cliente')
        
        if id_cliente is not None:
            try:
                cliente = ClienteContrato.objects.get(id_cliente=id_cliente)
                serializer = ClienteContratoSerializer(cliente, data=request.data, partial=True)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except ClienteContrato.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "ID do cliente não fornecido."}, status=status.HTTP_400_BAD_REQUEST)


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
                    forma_pagamento = linha['Forma de Pagamento'],
                    num_instalacao = linha['Número Instalação']
                )

    def inserir_faturas_do_csv(self, caminho_do_csv):
        with default_storage.open(caminho_do_csv, 'r') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            for linha in leitor_csv:
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
                demanda_pt = linha['Demanda PT (kW)']
                demanda_fp_cap = linha['Demanda FP CAP (kW)']
                demanda_fp_ind = linha['Demanda FP IND (kW)']
                consumo_pt_vd = consumo_pt_vd
                consumo_fp_cap_vd = consumo_fp_cap_vd
                consumo_fp_ind_vd = consumo_fp_ind_vd
                taxa_rev_fatura = taxa_rev_fatura
                tarifas = linha['Tarifa Energia Reativa PT C/ Imposto']
                grupo = linha['grupo']
                tipo_consumidor = linha['Código de Consumidor']
                num_instalacao = linha['Número Instalação']
                num_contrato = linha['Número Contrato']
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
                    demanda_pt = demanda_pt,
                    demanda_fp_cap = demanda_fp_cap,
                    demanda_fp_ind = demanda_fp_ind,
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
        


class AllEnergiaDataAPIView(APIView):
    def get(self, request, format=None):
        fatos_contrato = FatoContratoEnergia.objects.all()
        fatos_contrato_data = FatoContratoEnergiaSerializer(fatos_contrato, many=True).data
        
        clientes_contrato = ClienteContrato.objects.all()
        clientes_contrato_data = ClienteContratoSerializer(clientes_contrato, many=True).data
        
        enderecos_energia = EnderecoEnergia.objects.filter(num_contrato__in=[cliente['num_contrato'] for cliente in clientes_contrato_data])
        enderecos_energia_data = EnderecoSerializer(enderecos_energia, many=True).data
        
        fornecedores_energia = FornecedorEnergia.objects.filter(num_contrato__in=[cliente['num_contrato'] for cliente in clientes_contrato_data])
        fornecedores_energia_data = FornecedorEnergiaSerializer(fornecedores_energia, many=True).data
        
        combined_data = []
        for cliente in clientes_contrato_data:
            num_instalacao = cliente['num_instalacao']
            fatos_contrato_cliente = [fato for fato in fatos_contrato_data if fato['num_instalacao'] == num_instalacao]
            endereco_cliente = [endereco for endereco in enderecos_energia_data if endereco['num_contrato'] == cliente['num_contrato']]
            fornecedor_cliente = [fornecedor for fornecedor in fornecedores_energia_data if fornecedor['num_contrato'] == cliente['num_contrato']]
            
            combined_data.append({
                'cliente': cliente,
                'fatos_contrato': fatos_contrato_cliente,
                'endereco': endereco_cliente[0] if endereco_cliente else None,
                'fornecedor': fornecedor_cliente[0] if fornecedor_cliente else None
            })

        return Response(combined_data)