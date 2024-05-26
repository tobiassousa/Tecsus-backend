from django.urls import path
from energia.views import InserirDadosAPIView, EnderecoEnergiaAPIView, FornecedorEnergiaAPIView, ClienteContratoAPIView, FatoContratoEnergiaAPIView, AllEnergiaDataAPIView

urlpatterns = [
    path('upload/', InserirDadosAPIView.as_view(), name='upload_csv'),
    path('fornecedores_energia/', FornecedorEnergiaAPIView.as_view(), name='fornecedores_energia_api'),
    path('fornecedores_energia/<int:id_fornecedor_energia>', FornecedorEnergiaAPIView.as_view(), name='fornecedores_energia_by_id_api'),
    path('enderecos/', EnderecoEnergiaAPIView.as_view(), name='enderecos_api'),
    path('clientes_contratos/', ClienteContratoAPIView.as_view(), name='clientes_contratos_api'),
    path('clientes_contratos/<int:id_cliente>', ClienteContratoAPIView.as_view(), name='clientes_contratos_by_id_api'),
    path('fatos_contratos_energia/', FatoContratoEnergiaAPIView.as_view(), name='fatos_contratos_energia_api'),
    path('all_data/', AllEnergiaDataAPIView.as_view(), name='all_data_api'),
    # path('compare/<int:num_contrato>/', CompareMesAtualComTresUltimosMeses.as_view(), name='compare_current_month_to_last_three_months'),
]
