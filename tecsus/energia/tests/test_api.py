import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from energia.models import FornecedorEnergia

@pytest.mark.django_db
@pytest.mark.integration
def test_post_fornecedor():
    client = APIClient()
    url = reverse('fornecedores_energia_api')
    data = {
        "fornecedor": "Fornecedor Teste",
        "num_contrato": 123456789
    }
    
    response = client.post(url, data, format='json')
    
    assert response.status_code == 201
    assert response.data['fornecedor'] == data['fornecedor']
    assert response.data['num_contrato'] == data['num_contrato']
    
@pytest.mark.django_db
@pytest.mark.integration
def test_get_all_fornecedor():
    client = APIClient()

    # Criar múltiplas instâncias de FornecedorEnergia
    fornecedor1 = FornecedorEnergia.objects.create(
        fornecedor="Fornecedor Teste 1",
        num_contrato=123456789
    )
    fornecedor2 = FornecedorEnergia.objects.create(
        fornecedor="Fornecedor Teste 2",
        num_contrato=987654321
    )

    # Listar todos os fornecedores
    url = reverse('fornecedores_energia_api')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['fornecedor'] == fornecedor1.fornecedor
    assert response.data[1]['fornecedor'] == fornecedor2.fornecedor