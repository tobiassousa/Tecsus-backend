import pytest
from decimal import Decimal
from datetime import date
from agua.models import FornecedorAgua, Endereco, ClienteContrato, FatoContratoAgua

@pytest.mark.django_db
@pytest.mark.unit
def test_fornecedor_agua_creation():
    fornecedor = FornecedorAgua.objects.create(
        fornecedor="Companhia de Água",
        cod_companhia="123456",
        planta="Planta A",
        codigo_de_ligacao_rgi="RGI12345"
    )
    assert fornecedor.id_fornecedor_agua is not None
    assert fornecedor.fornecedor == "Companhia de Água"

@pytest.mark.django_db
@pytest.mark.unit
def test_endereco_creation():
    endereco = Endereco.objects.create(
        endereco_instalacao="Rua A, 123",
        cidade="Cidade X"
    )
    assert endereco.id_endereco is not None
    assert endereco.endereco_instalacao == "Rua A, 123"

@pytest.mark.django_db
@pytest.mark.unit
def test_cliente_contrato_creation():
    cliente = ClienteContrato.objects.create(
        nome_contrato="Contrato A",
        email="cliente@example.com",
        ativo="Sim",
        numero_contrato=1234567890,
        numero_cliente=9876543210,
        codigo_de_ligacao_rgi="RGI12345"
    )
    assert cliente.numero_contrato == 1234567890
    assert cliente.email == "cliente@example.com"

@pytest.mark.django_db
@pytest.mark.unit
def test_fato_contrato_agua_creation():
    endereco = Endereco.objects.create(
        endereco_instalacao="Rua A, 123",
        cidade="Cidade X"
    )
    cliente = ClienteContrato.objects.create(
        nome_contrato="Contrato A",
        email="cliente@example.com",
        ativo="Sim",
        numero_contrato=1234567890,
        numero_cliente=9876543210,
        codigo_de_ligacao_rgi="RGI12345"
    )
    fato_contrato = FatoContratoAgua.objects.create(
        codigo_de_ligacao_rgi=cliente,
        id_endereco=endereco,
        consumo_agua_m3=Decimal('100.50'),
        consumo_esgoto_m3=Decimal('75.25'),
        vlr_agua=Decimal('150.75'),
        vlr_esgoto=Decimal('50.25'),
        vlr_total=Decimal('201.00'),
        leitura_anterior=date(2023, 1, 1),
        leitura_atual=date(2023, 1, 31)
    )
    assert fato_contrato.id_contrato_agua is not None
    assert fato_contrato.consumo_agua_m3 == Decimal('100.50')
    assert fato_contrato.vlr_total == Decimal('201.00')
  