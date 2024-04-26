@echo off

REM Construir conteineres Docker
echo Construindo contêineres Docker...
docker-compose build

REM Aplicar migraçoes do Django
echo Aplicando migrações do Django...
docker-compose run web python manage.py makemigrate

REM Aplicar migracoes do Django
echo Aplicando migrações do Django...
docker-compose run web python manage.py migrate

REM Criar superusuario
echo Criando superusuário...
docker-compose run web python manage.py createsuperuser
echo Superusuário criado com sucesso.

echo Instalação concluída.
