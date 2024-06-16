from datetime import datetime, timedelta
from django.db.models import Avg
from .models import FatoContratoEnergia

def calcular_media_ultimos_tres_meses(num_instalacao):
    hoje = datetime.now()
    tres_meses_atras = hoje - timedelta(days=90)
    tres_meses_atras = datetime(tres_meses_atras.year, tres_meses_atras.month, 1)

    media_ultimos_tres_meses = FatoContratoEnergia.objects.filter(
        num_instalacao=num_instalacao,
        leitura_atual__gte=tres_meses_atras,
        leitura_atual__lt=hoje
    ).aggregate(Avg('total'))

    return media_ultimos_tres_meses['total__avg'] or 0

def calcular_media_mes_atual(num_instalacao):
    hoje = datetime.now()
    primeiro_dia_do_mes = datetime(hoje.year, hoje.month, 1)
    proximo_mes = hoje.month % 12 + 1
    proximo_ano = hoje.year + (hoje.month // 12)
    primeiro_dia_proximo_mes = datetime(proximo_ano, proximo_mes, 1)
    
    media_mes_atual = FatoContratoEnergia.objects.filter(
        num_instalacao=num_instalacao,
        leitura_atual__gte=primeiro_dia_do_mes,
        leitura_atual__lt=primeiro_dia_proximo_mes
    ).aggregate(Avg('total'))

    return media_mes_atual['total__avg'] or 0

def comparar_media_mes_atual_com_ultimos_tres_meses(num_instalacao):
    media_ultimos_tres_meses = calcular_media_ultimos_tres_meses(num_instalacao)
    media_mes_atual = calcular_media_mes_atual(num_instalacao)

    if media_mes_atual > media_ultimos_tres_meses:
        return "O valor médio deste mês é maior que a média dos últimos três meses."
    elif media_mes_atual < media_ultimos_tres_meses:
        return "O valor médio deste mês é menor que a média dos últimos três meses."
    else:
        return "O valor médio deste mês é igual à média dos últimos três meses."
