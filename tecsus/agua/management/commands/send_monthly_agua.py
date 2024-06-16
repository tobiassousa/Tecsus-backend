from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from agua.models import FatoContratoAgua
from alerta.models import AlertaAgua
from agua.utils import comparar_media_mes_atual_com_ultimos_tres_meses, calcular_media_ultimos_tres_meses, calcular_media_mes_atual
from datetime import datetime
from decouple import config

class Command(BaseCommand):
    help = 'Envia e-mails mensais para clientes e salva alertas no banco de dados'

    def handle(self, *args, **options):
        clientes = set(FatoContratoAgua.objects.values_list('codigo_de_ligacao_rgi', flat=True))

        for cliente in clientes:
            resultado_comparacao = comparar_media_mes_atual_com_ultimos_tres_meses(cliente)
            if "igual à média" in resultado_comparacao:
                media_tres_meses = calcular_media_ultimos_tres_meses(cliente)
                media_mes_atual = calcular_media_mes_atual(cliente)
                self.salvar_alerta(cliente, media_tres_meses, media_mes_atual)
                self.enviar_email(cliente, media_tres_meses, media_mes_atual)

        self.stdout.write(self.style.SUCCESS('Processo concluído'))

    def salvar_alerta(self, codigo_de_ligacao_rgi, media_tres_meses, media_mes_atual):
        data_atual = datetime.now()

        AlertaAgua.objects.create(
            id_user_alerta=codigo_de_ligacao_rgi,
            alert_user_email="ariane.crisousa@gmail.com",
            alert_consumo_media=media_tres_meses,
            alert_consumo_atual=media_mes_atual,
            alert_conta=data_atual.strftime("1/%m/%Y")
        )
        self.stdout.write(self.style.SUCCESS('Alerta salvo para o cliente {}.'.format(codigo_de_ligacao_rgi)))

    def enviar_email(self, codigo_de_ligacao_rgi, media_tres_meses, media_mes_atual):
        assunto = "Alerta de Consumo de Água"
        contexto = {
            'codigo_de_ligacao_rgi': codigo_de_ligacao_rgi,
            'media_tres_meses': "R$ " + "{:.2f}".format(media_tres_meses) if media_tres_meses is not None else None,
            'media_mes_atual': "R$ " + "{:.2f}".format(media_mes_atual) if media_mes_atual is not None else None,
            'mensagem': "O valor médio deste mês é igual à média dos últimos três meses."
        }

        corpo_email_html = render_to_string('email/envio_email.html', contexto)
        corpo_email_texto = strip_tags(corpo_email_html)

        send_mail(
            subject=assunto,
            message=corpo_email_texto,
            html_message=corpo_email_html,
            from_email=config('EMAIL', default=''),
            recipient_list=['ariane.crisousa@gmail.com'],
        )
        self.stdout.write(self.style.SUCCESS('E-mail enviado para o cliente {}.'.format(codigo_de_ligacao_rgi)))
