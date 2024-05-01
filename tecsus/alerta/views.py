from rest_framework import status
from alerta.serializer import AlertaAguaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AlertaAgua


class AlertaAguaAPIView(APIView):
    def get(self, request):
        alerta_agua = AlertaAgua.objects.all()
        data = [{'id_alerta': alerta_agua.id_alerta,
                 'id_user_alerta': alerta_agua.id_user_alerta,
                 'alert_user_email': alerta_agua.alert_user_email,
                 'alert_consumo_media': alerta_agua.alert_consumo_media,
                 'alert_consumo_atual': alerta_agua.alert_consumo_atual,
                 'alert_conta': alerta_agua.alert_conta,
                }]
        return Response(data) 
    
    def post(self, request):
        serializer = AlertaAguaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        