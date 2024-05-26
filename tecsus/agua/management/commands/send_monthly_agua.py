from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from agua.models import FatoContratoAgua
from alerta.models import AlertaAgua
from agua.utils import calcular_media_ultimos_tres_meses, verificar_consumo_mes_anterior
from datetime import datetime
from decouple import config

class Command(BaseCommand):
    help = 'Envia e-mails mensais para clientes e salva alertas no banco de dados'

    def handle(self, *args, **options):
        clientes = set(FatoContratoAgua.objects.values_list('codigo_de_ligacao_rgi', flat=True))

        for cliente in clientes:
            resultado_verificacao = verificar_consumo_mes_anterior(cliente)
            if resultado_verificacao:
                media_tres_meses = calcular_media_ultimos_tres_meses(cliente)
                if media_tres_meses is not None:
                    if "maior que a média" in resultado_verificacao:
                        self.salvar_alerta(cliente, media_tres_meses, resultado_verificacao)
                        self.enviar_email(cliente,  media_tres_meses, resultado_verificacao)

        self.stdout.write(self.style.ERROR('Sem envio de alertas'))


    def salvar_alerta(self, codigo_de_ligacao_rgi, media_tres_meses, resultado_verificacao):
        data_atual = datetime.now()

        AlertaAgua.objects.create(
            id_user_alerta=codigo_de_ligacao_rgi,
            alert_user_email= "ariane.crisousa@gmail.com",
            alert_consumo_media=media_tres_meses,
            alert_consumo_atual=resultado_verificacao,
            alert_conta=data_atual.strftime("1/%m/%Y")
        )
        self.stdout.write(self.style.SUCCESS('Alerta salvo para o cliente {}.'.format(codigo_de_ligacao_rgi)))

    def enviar_email(self, codigo_de_ligacao_rgi, media_tres_meses, resultado_verificacao):
        assunto = "Alerta de Consumo de Água"
        contexto = {
            'codigo_de_ligacao_rgi': codigo_de_ligacao_rgi,
            'media_tres_meses': "R$ " + "{:.2f}".format(media_tres_meses) if media_tres_meses is not None else None,
            'resultado_verificacao': resultado_verificacao
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
