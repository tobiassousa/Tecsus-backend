from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from energia.models import ProEnergia
from alerta.models import AlertaAgua
from energia.utils import calcular_media_ultimos_tres_meses, verificar_consumo_mes_anterior
from datetime import datetime
from decouple import config

class Command(BaseCommand):
    help = 'Envia e-mails mensais para clientes e salva alertas no banco de dados'

    def handle(self, *args, **options):
        clientes = set(ProEnergia.objects.values_list('num_cliente', flat=True))

        for num_cliente in clientes:
            resultado_verificacao = verificar_consumo_mes_anterior(num_cliente)
            if resultado_verificacao:
                media_tres_meses = calcular_media_ultimos_tres_meses(num_cliente)
                if media_tres_meses is not None:
                    # if "maior que a média" in resultado_verificacao:
                        self.salvar_alerta(num_cliente, media_tres_meses, resultado_verificacao)
                        self.enviar_email(num_cliente,  media_tres_meses, resultado_verificacao)

        self.stdout.write(self.style.ERROR('Sem envio de alertas'))


    def salvar_alerta(self, num_cliente, media_tres_meses, resultado_verificacao):
        data_atual = datetime.now()

        AlertaAgua.objects.create(
            id_user_alerta=num_cliente,
            alert_user_email= "ariane.crisousa@gmail.com",
            alert_consumo_media=media_tres_meses,
            alert_consumo_atual=resultado_verificacao,
            alert_conta=data_atual.strftime("1/%m/%Y")
        )
        self.stdout.write(self.style.SUCCESS('Alerta salvo para o cliente {}.'.format(num_cliente)))

    def enviar_email(self, num_cliente, media_tres_meses, resultado_verificacao):
        assunto = "Alerta de Consumo de Água"
        contexto = {
            'num_cliente': num_cliente,
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
        self.stdout.write(self.style.SUCCESS('E-mail enviado para o cliente {}.'.format(num_cliente)))
