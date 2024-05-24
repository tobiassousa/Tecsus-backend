from rest_framework import serializers
from .models import FornecedorEnergia, EnderecoEnergia, FatoContratoEnergia, ClienteContrato


class FornecedorEnergiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FornecedorEnergia
        fields = '__all__'

        
class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnderecoEnergia
        fields = '__all__'


class FatoContratoEnergiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatoContratoEnergia
        fields = '__all__'


class ClienteContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteContrato
        fields = '__all__'
