import csv
from django.shortcuts import render
from .forms import CSVUploadForm
from .models import Agua, Energia, Gas
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

class UploadCSVView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, model, documento):
        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)
                headers = next(reader)
                model_class = self.get_model_class(model)
                if model_class is not None:
                    for row in reader:
                        dados = {}
                        for idx, value in enumerate(row):
                            field_name = headers[idx]
                            dados[field_name] = value
                        novo_dado = model_class.objects.create(dados=dados, documento=documento)
                    return Response("Upload realizado com sucesso!", status=200)
                else:
                    return Response("Modelo inválido.", status=400)
        else:
            form = CSVUploadForm()
        return Response("Falha no upload do CSV.", status=400)

    def get_model_class(self, model):
        if model == 'agua':
            return Agua
        elif model == 'energia':
            return Energia
        elif model == 'gas':
            return Gas
        else:
            return None

