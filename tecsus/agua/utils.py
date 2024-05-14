from datetime import datetime, timedelta
from django.db.models import Avg
from .models import FatoContratoAgua

def calcular_media_ultimos_tres_meses(cod_ligacao_rgi):
    hoje = datetime.now()
    tres_meses_atras = hoje - timedelta(days=90)
    tres_meses_atras = datetime(tres_meses_atras.year, tres_meses_atras.month, 1)

    media_ultimos_tres_meses = FatoContratoAgua.objects.filter(
        codigo_de_ligacao_rgi=cod_ligacao_rgi,
        leitura_atual__gte=tres_meses_atras,
        leitura_atual__lt=hoje
    ).aggregate(Avg('vlr_total'))

    return media_ultimos_tres_meses['vlr_total__avg'] or 0

def calcular_media_mes_atual(cod_ligacao_rgi):
    hoje = datetime.now()
    primeiro_dia_do_mes = datetime(hoje.year, hoje.month, 1)
    proximo_mes = hoje.month % 12 + 1
    proximo_ano = hoje.year + (hoje.month // 12)
    primeiro_dia_proximo_mes = datetime(proximo_ano, proximo_mes, 1)
    
    media_mes_atual = FatoContratoAgua.objects.filter(
        codigo_de_ligacao_rgi=cod_ligacao_rgi,
        leitura_atual__gte=primeiro_dia_do_mes,
        leitura_atual__lt=primeiro_dia_proximo_mes
    ).aggregate(Avg('vlr_total'))

    return media_mes_atual['vlr_total__avg'] or 0

def comparar_media_mes_atual_com_ultimos_tres_meses(cod_ligacao_rgi):
    media_ultimos_tres_meses = calcular_media_ultimos_tres_meses(cod_ligacao_rgi)
    media_mes_atual = calcular_media_mes_atual(cod_ligacao_rgi)

    if media_mes_atual > media_ultimos_tres_meses:
        return "O valor médio deste mês é maior que a média dos últimos três meses."
    elif media_mes_atual < media_ultimos_tres_meses:
        return "O valor médio deste mês é menor que a média dos últimos três meses."
    else:
        return "O valor médio deste mês é igual à média dos últimos três meses."
