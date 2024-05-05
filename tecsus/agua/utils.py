from datetime import datetime, timedelta
from .models import ProAgua

def corrigir_e_converter(valor_str):
    valor_str = valor_str.strip().replace('.', '').replace(',', '.')
    try:
        return float(valor_str)
    except ValueError:
        return 0.0

def calcular_media_ultimos_tres_meses(num_cliente):
    data_tres_meses_atras = datetime.now() - timedelta(days=90)

    registros = ProAgua.objects.filter(
        num_cliente=num_cliente,
        leitura_atual__gte=data_tres_meses_atras
    )

    valores_corrigidos = []
    for registro in registros:
        valor_corrigido = corrigir_e_converter(registro.vlw_total)
        if valor_corrigido is not None:
            valores_corrigidos.append(valor_corrigido)

    if valores_corrigidos:
        media = sum(valores_corrigidos) / len(valores_corrigidos)
        return media
    else:
        return None

def verificar_consumo_mes_anterior(num_cliente):
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
    ano_anterior = ano_atual if mes_atual > 1 else ano_atual - 1

    data_mes_anterior = datetime(ano_anterior, mes_anterior, 1)
    data_inicio_mes_atual = datetime(ano_atual, mes_atual, 1)
    registros_mes_anterior = ProEnergia.objects.filter(
        num_cliente=num_cliente,
        leitura_atual__gte=data_mes_anterior,
        leitura_atual__lt=data_inicio_mes_atual
    )

    valores_corrigidos = []
    for registro in registros_mes_anterior:
        valor_corrigido = corrigir_e_converter(registro.vlw_total)
        if valor_corrigido is not None:
            valores_corrigidos.append(valor_corrigido)

    if valores_corrigidos:
        consumo_mes_anterior = sum(valores_corrigidos)
        media_ultimos_tres_meses = calcular_media_ultimos_tres_meses(num_cliente)
        if media_ultimos_tres_meses is not None:
            if consumo_mes_anterior > media_ultimos_tres_meses:
                return f"O consumo do mês anterior ({datetime.strftime(data_mes_anterior, '%B')}) foi maior que a média dos últimos três meses."
            else:
                return f"O consumo do mês anterior ({datetime.strftime(data_mes_anterior, '%B')}) foi menor ou igual à média dos últimos três meses."
        else:
            return "Não foi possível calcular a média dos últimos três meses."
    else:
        return "Não há registros para o mês anterior."

