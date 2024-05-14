from rest_framework import serializers
from .models import FornecedorAgua, Endereco, ClienteContrato, FatoContratoAgua


class FornecedorAguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FornecedorAgua
        fields = '__all__'


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'


class ClienteContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteContrato
        fields = '__all__'


class FatoContratoAguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatoContratoAgua
        fields = '__all__'
