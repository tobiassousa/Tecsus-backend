from rest_framework import status
from alerta.serializer import AlertaAguaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AlertaAgua


class AlertaAguaAPIView(APIView):
    def get(self, request):
        alertas = AlertaAgua.objects.all()
        serializer = AlertaAguaSerializer(alertas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AlertaAguaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        