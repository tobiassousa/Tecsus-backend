from rest_framework.views import APIView
from rest_framework.response import Response
from agua.serializer import AlertaAguaSerializer
from .models import AlertaAgua, ContratoAgua, ProAgua
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

class ContratoAguaAPIView(APIView):
    def get(self, request):
        contratos_agua = ContratoAgua.objects.all()
        data = [{'id': contrato.id_contrato_agua,
                 'fornecedor': contrato.fornecedor,
                 'num_instalacao': contrato.num_instalacao,
                 'num_medidor': contrato.num_medidor,
                 'num_cliente': contrato.num_cliente,
                 'modalidade': contrato.modalidade,
                 'num_contrato': contrato.num_contrato,
                 'tipo_pagto': contrato.tipo_pagto,
                 'email_agua': contrato.email_agua,
                 'cidade': contrato.cidade,
                 'cod_ligacao_rgi': contrato.cod_ligacao_rgi,
                 'data_extra': contrato.data_extra} for contrato in contratos_agua]
        return Response(data)

class ProAguaAPIView(APIView):
    def get(self, request):
        pros_agua = ProAgua.objects.all()
        data = [{'id': pro.id_pro_agua,
                 'leitura_anterior': pro.leitura_anterior,
                 'leitura_atual': pro.leitura_atual,
                 'consumo_agua_m3': pro.consumo_agua_m3,
                 'consumo_esgoto_m3': pro.consumo_esgoto_m3,
                 'vlr_agua': pro.vlr_agua,
                 'vlr_esgoto': pro.vlr_esgoto,
                 'vlr_total': pro.vlr_total,
                 'num_instalacao': pro.num_instalacao,
                 'num_medidor': pro.num_medidor,
                 'num_cliente': pro.num_cliente,
                 'cod_ligacao_rgi': pro.cod_ligacao_rgi,
                 'num_contrato': pro.num_contrato,
                 'data_extra': pro.data_extra} for pro in pros_agua]
        return Response(data)
    
class AlertaAguaAPIView(APIView):
    def get(self, request):
        alertas = AlertaAgua.objects.all()
        serializer = AlertaAguaSerializer(alertas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AlertaAguaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@require_http_methods(["GET"])
def consulta_contrato_pro_agua(request):
    resultados = ContratoAgua.objects.raw('''
        SELECT ct.id_contrato_agua, ct.fornecedor, ct.num_instalacao, ct.num_medidor, ct.num_cliente,
               ct.modalidade, ct.num_contrato, ct.tipo_pagto, ct.email_agua,
               ct.cidade, ct.cod_ligacao_rgi, pr.id_pro_agua, pr.leitura_anterior, pr.leitura_atual,
               pr.consumo_agua_m3, pr.consumo_esgoto_m3, pr.vlr_agua, pr.vlr_esgoto,
               pr.vlr_total, pr.num_instalacao, pr.num_medidor, pr.num_cliente,
               pr.cod_ligacao_rgi, pr.num_contrato
        FROM agua_contratoagua ct
        INNER JOIN agua_proagua pr ON pr.cod_ligacao_rgi = ct.cod_ligacao_rgi
    ''')

    data = []
    for resultado in resultados:
        data.append({
            'id_contrato_agua': resultado.id_contrato_agua,
            'fornecedor': resultado.fornecedor,
            'num_instalacao': resultado.num_instalacao,
            'num_medidor': resultado.num_medidor,
            'num_cliente': resultado.num_cliente,
            'modalidade': resultado.modalidade,
            'num_contrato': resultado.num_contrato,
            'tipo_pagto': resultado.tipo_pagto,
            'email_agua': resultado.email_agua,
            'cidade': resultado.cidade,
            'cod_ligacao_rgi': resultado.cod_ligacao_rgi,
            'id_pro_agua': resultado.id_pro_agua,
            'leitura_anterior': resultado.leitura_anterior,
            'leitura_atual': resultado.leitura_atual,
            'consumo_agua_m3': resultado.consumo_agua_m3,
            'consumo_esgoto_m3': resultado.consumo_esgoto_m3,
            'vlr_agua': resultado.vlr_agua,
            'vlr_esgoto': resultado.vlr_esgoto,
            'vlr_total': resultado.vlr_total,
            'num_instalacao_pro': resultado.num_instalacao,
            'num_medidor_pro': resultado.num_medidor,
            'num_cliente_pro': resultado.num_cliente,
            'cod_ligacao_rgi_pro': resultado.cod_ligacao_rgi,
            'num_contrato_pro': resultado.num_contrato
        })

    return JsonResponse(data, safe=False)

