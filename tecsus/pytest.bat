@echo off

REM 
echo
cd tecsus

REM Rodando testes
echo Executando testes unitarios...
docker-compose run web pytest