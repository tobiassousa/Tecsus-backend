@echo off

REM Construir contêineres Docker
echo Construindo contêineres Docker...
docker-compose build

REM Aplicar migrações do Django
echo Aplicando migrações do Django...
docker-compose run web python manage.py makemigrations

REM Aplicar migrações do Django
echo Aplicando migrações do Django...
docker-compose run web python manage.py migrate

REM Criar superusuário
echo Criando superusuário...
docker-compose run web python manage.py createsuperuser
echo Superusuário criado com sucesso.

echo Instalação concluída.
