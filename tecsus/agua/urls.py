from django.urls import path
from agua.views import InserirDadosAPIView, FornecedorAguaAPIView, EnderecoAPIView, ClienteContratoAPIView, FatoContratoAguaAPIView, AllDataAPIView

urlpatterns = [
    path('upload/', InserirDadosAPIView.as_view(), name='upload_csv'),
    path('fornecedores_agua/', FornecedorAguaAPIView.as_view(), name='fornecedores_agua_api'),
    path('enderecos/', EnderecoAPIView.as_view(), name='enderecos_api'),
    path('clientes_contratos/', ClienteContratoAPIView.as_view(), name='clientes_contratos_api'),
    path('fatos_contratos_agua/', FatoContratoAguaAPIView.as_view(), name='fatos_contratos_agua_api'),
    path('all_data/', AllDataAPIView.as_view(), name='all_data_api'),
]