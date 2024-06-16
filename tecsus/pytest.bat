@echo off

REM Verifica se argumentos foram passados
IF "%~1"=="" (
    set TEST_MARKER=""
) ELSE (
    set TEST_MARKER="-m %~1"
)

IF "%~1"=="unit" (
    set TEST_TYPE=de unidade
) ELSE IF "%~1"=="integration" (
    set TEST_TYPE=de integracao
) ELSE (
    set TEST_TYPE=""
)

REM Rodando testes
echo Executando testes %TEST_TYPE%
docker-compose run web pytest %TEST_MARKER% -vv