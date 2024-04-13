@echo off

REM Aplicar migrações do Django
echo Aplicando migrações do Django...
docker-compose run web python manage.py makemigrations

REM Aplicar migrações do Django
echo Aplicando migrações do Django...
docker-compose run web python manage.py migrate

REM Iniciando contêineres Docker
echo Iniciando contêineres Docker...
docker-compose up
