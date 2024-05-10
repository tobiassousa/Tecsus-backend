from datetime import datetime, timedelta
from .models import ProEnergia

def corrigir_e_converter(valor_str):
    valor_sem_virgula = valor_str.split(".")[0]
    valor_sem_pontos = valor_sem_virgula.replace(",", "").strip()
    try:
        return float(valor_sem_pontos)
    except ValueError:
        return 0.0

def calcular_media_ultimos_tres_meses(num_cliente):
    data_tres_meses_atras = datetime.now() - timedelta(days=90)

    registros = ProEnergia.objects.filter(
        num_cliente=num_cliente,
        leitura_atual__gte=data_tres_meses_atras
    )

    valores_corrigidos = []
    for registro in registros:
        valor_corrigido = corrigir_e_converter(registro.total)
        if valor_corrigido is not None:
            valores_corrigidos.append(valor_corrigido)

    if valores_corrigidos:
        media = sum(valores_corrigidos) / len(valores_corrigidos)
        return media
    else:
        return None
    

def verificar_consumo_mes_anterior(num_cliente):
    registros = ProEnergia.objects.filter(
        num_cliente=num_cliente,
        leitura_atual__gte="08/05/2024", 
        leitura_atual__lte="30/05/2024"
    )

    valores_corrigidos = []
    for registro in registros:
        valor_corrigido = corrigir_e_converter(registro.total)
        if valor_corrigido is not None:
            valores_corrigidos.append(valor_corrigido)

    if valores_corrigidos:
        media = sum(valores_corrigidos) / len(valores_corrigidos)
        return media
    else:
        return None
    

def comparar_consumo_mes_atual_e_anterior(num_cliente):
    media_mes_atual = calcular_media_ultimos_tres_meses(num_cliente)
    media_mes_anterior = verificar_consumo_mes_anterior(num_cliente)

    if media_mes_atual is not None and media_mes_anterior is not None:
        if media_mes_atual > media_mes_anterior:
            return "O consumo deste mês é maior do que o consumo do mês anterior."
        elif media_mes_atual < media_mes_anterior:
            return "O consumo deste mês é menor do que o consumo do mês anterior."
        else:
            return "O consumo deste mês é igual ao consumo do mês anterior."
    else:
        return "Não foi possível comparar os consumos."
    


