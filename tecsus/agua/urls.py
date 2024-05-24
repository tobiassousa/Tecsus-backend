from django.urls import path

from agua.views import InserirDadosAPIView, FornecedorAguaAPIView, EnderecoAPIView, ClienteContratoAPIView, FatoContratoAguaList, AllDataAPIView, CompareMesAtualComTresUltimosMeses, AllDataAPIView

urlpatterns = [
    path('upload/', InserirDadosAPIView.as_view(), name='upload_csv'),
    path('fornecedores_agua/', FornecedorAguaAPIView.as_view(), name='fornecedores_agua_api'),
    path('enderecos/', EnderecoAPIView.as_view(), name='enderecos_api'),
    path('clientes_contratos/', ClienteContratoAPIView.as_view(), name='clientes_contratos_api'),
    path('fatos_contratos_agua/', FatoContratoAguaList.as_view(), name='fatos_contratos_agua_api'),
    path('all_data/', AllDataAPIView.as_view(), name='all_data_api'),
    path('compare/<str:codigo_de_ligacao_rgi>/', CompareMesAtualComTresUltimosMeses.as_view(), name='compare_current_month_to_last_three_months'),
]