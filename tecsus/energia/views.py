from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AlertaEnergia, ContratoEnergia, ProEnergia
from energia.serializer import AlertaEnergiaSerializer

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

class ContratoEnergiaAPIView(APIView):
    def get(self, request):
        contratos_energia = ContratoEnergia.objects.all()
        data = [{'id': contrato.id_contrato_energia,
                 'fornecedor': contrato.fornecedor,
                 'num_instalacao': contrato.num_instalacao,
                 'num_medidor': contrato.num_medidor,
                 'num_cliente': contrato.num_cliente,
                 'modalidade': contrato.modalidade,
                 'forma_pagto': contrato.forma_pagto,
                 'email_energia': contrato.email_energia,
                 'cidade': contrato.cidade,
                 'num_contrato': contrato.num_contrato,
                 'data_extra': contrato.data_extra} for contrato in contratos_energia]
        return Response(data)


class ProEnergiaAPIView(APIView):
    def get(self, request):
        pro_energias = ProEnergia.objects.all()
        data = [{'id': pro.id_pro_energia,
                 'leitura_anterior': pro.leitura_anterior,
                 'leitura_atual': pro.leitura_atual,
                 'demanda_faturada_kw': pro.demanda_faturada_kw,
                 'total': pro.total,
                 'fornecedor': pro.fornecedor,
                 'num_instalacao': pro.num_instalacao,
                 'num_cliente': pro.num_cliente,
                 'modalidade': pro.modalidade,
                 'num_contrato': pro.num_contrato,
                 'data_extra': pro.data_extra} for pro in pro_energias]
        return Response(data)
    
class AlertaEnergiaAPIView(APIView):
    def get(self, request):
        alertas = AlertaEnergia.objects.all()
        serializer = AlertaEnergiaSerializer(alertas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AlertaEnergiaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@require_http_methods(["GET"])
def consulta_contrato_pro_energia(request):
    resultados = ContratoEnergia.objects.raw('''
        SELECT tce.id_contrato_energia, tce.fornecedor, tce.num_instalacao, tce.num_medidor,
               tce.num_cliente, tce.modalidade, tce.forma_pagto, tce.cidade, pe.id_pro_energia,
               pe.leitura_anterior, pe.leitura_atual, pe.demanda_faturada_kw, pe.total,
               pe.fornecedor, pe.num_instalacao, pe.num_cliente, pe.modalidade,
               pe.num_contrato
        FROM energia_contratoenergia tce
        INNER JOIN energia_proenergia pe ON pe.num_instalacao = tce.num_instalacao
        WHERE pe.num_contrato <> ''
    ''')

    data = []
    for resultado in resultados:
        data.append({
            'id_contrato_energia': resultado.id_contrato_energia,
            'fornecedor_contrato': resultado.fornecedor,
            'num_instalacao_contrato': resultado.num_instalacao,
            'num_medidor_contrato': resultado.num_medidor,
            'num_cliente_contrato': resultado.num_cliente,
            'modalidade_contrato': resultado.modalidade,
            'forma_pagto_contrato': resultado.forma_pagto,
            'cidade': resultado.cidade,
            'id_pro_energia': resultado.id_pro_energia,
            'leitura_anterior_energia': resultado.leitura_anterior,
            'leitura_atual_energia': resultado.leitura_atual,
            'demanda_faturada_kw': resultado.demanda_faturada_kw,
            'total': resultado.total,
            'fornecedor_energia': resultado.fornecedor,
            'num_instalacao_energia': resultado.num_instalacao,
            'num_cliente_energia': resultado.num_cliente,
            'modalidade_energia': resultado.modalidade,
            'num_contrato_energia': resultado.num_contrato
        })

    return JsonResponse(data, safe=False)

    
