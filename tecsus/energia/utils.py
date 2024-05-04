from datetime import datetime, timedelta
from django.db.models import Avg
from .models import ProEnergia

def corrigir_e_converter(valor_str):
    valor_str = valor_str.strip().replace(',', '.')
    try:
        return float(valor_str)
    except ValueError:
        return 0.0


def calcular_media_ultimos_tres_meses(num_cliente):
    data_tres_meses_atras = datetime.now() - timedelta(days=90)
    print(data_tres_meses_atras)

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
