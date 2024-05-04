import csv
from .forms import CSVUploadForm
from agua.models import ContratoAgua, ProAgua
from energia.models import ContratoEnergia, ProEnergia
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config

class UploadCSVView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, model, documento):
        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                model_class = self.get_model_class(model, documento)
                if model_class is not None:
                    for row in reader:
                        dados = {}
                        data_extra = {}
                        for csv_header, csv_value in row.items():
                            model_field = self.get_model_field(model_class, csv_header, model, documento)                           
                            if model_field:
                                dados[model_field] = csv_value
                            else:
                                data_extra[csv_header] = csv_value
                        model_class.objects.create(**dados, data_extra=data_extra)
                    return Response("Upload realizado com sucesso!", status=200)
                else:
                    return Response("Modelo ou documento inválido.", status=400)
        else:
            form = CSVUploadForm()
        return Response("Falha no upload do CSV.", status=400)

    def get_model_class(self, model, documento):
        if model == 'energia':
            return ProEnergia if documento == 'fatura' else ContratoEnergia
        elif model == 'agua':
            return ProAgua if documento == 'fatura' else ContratoAgua
        else:
            return None
    
    def get_model_field(self, model_class, csv_header, model, documento):
        field_mapping_energia_contrato = {
            'Fornecedor': 'fornecedor',
            'Número Instalação': 'num_instalacao',
            'Número Medidor': 'num_medidor',
            'Número Cliente': 'num_cliente',
            'Modalidade': 'modalidade',
            'Número Contrato': 'num_contrato',
            'Forma de Pagamento': 'forma_pagto',
            'Campo Extra de Acesso 1': 'email_energia',
            'Nome do Contrato': 'cidade',
        }

        field_mapping_energia_pro = {
            'Leitura Anterior': 'leitura_anterior',
            'Leitura Atual': 'leitura_atual',
            'Demanda Faturada (kW)': 'demanda_faturada_kw',
            'Total': 'total',
            'Fornecedor': 'fornecedor',
            'Número Instalação': 'num_instalacao',
            'Número Cliente': 'num_cliente',
            'Modalidade': 'modalidade',
            'Número Contrato': 'num_contrato',
        }

        field_mapping_agua_contrato = {
            'Fornecedor': 'fornecedor',
            'Número Instalação': 'num_instalacao',
            'Número Medidor': 'num_medidor',
            'Número Cliente': 'num_cliente',
            'Modalidade': 'modalidade',
            'Número Contrato': 'num_contrato',
            'Forma de Pagamento': 'tipo_pagto',
            'Campo Extra de Acesso 1': 'email_agua',
            'Nome do Contrato': 'cidade',
            'Código de Ligação (RGI)': 'cod_ligacao_rgi',
        }

        field_mapping_agua_pro = {
            'Leitura Anterior': 'leitura_anterior',
            'Leitura Atual': 'leitura_atual',
            'Consumo de Água m³': 'consumo_agua_m3',
            'Consumo de Esgoto m³': 'consumo_esgoto_m3',
            'Valor Água R$': 'vlr_agua',
            'Valor Esgoto R$': 'vlr_esgoto',
            'Total R$': 'vlr_total',
            'Número Instalação': 'num_instalacao',
            'Número Medidor': 'num_medidor',
            'Número Cliente': 'num_cliente',
            'Código de Ligação (RGI)': 'cod_ligacao_rgi',
            'Número Contrato': 'num_contrato',
        }

        if model == 'energia':
            if documento == 'contrato':
                return field_mapping_energia_contrato.get(csv_header, None)
            elif documento == 'fatura':
                return field_mapping_energia_pro.get(csv_header, None)
        elif model == 'agua':
            if documento == 'contrato':
                return field_mapping_agua_contrato.get(csv_header, None)
            elif documento == 'fatura':
                return field_mapping_agua_pro.get(csv_header, None)
        return None



class EnviarEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, email):
        assunto = "Alerta"
        contexto = request.data.get('contexto', {})

        corpo_email_html = render_to_string('email/envio_email.html', contexto)

        corpo_email_texto = strip_tags(corpo_email_html)

        send_mail(
            subject=assunto,
            message=corpo_email_texto,
            html_message=corpo_email_html,
            from_email= config('EMAIL_HOST_USER', default=''),
            recipient_list=[email],
        )
        return Response({'status': 'E-mail enviado com sucesso'})
