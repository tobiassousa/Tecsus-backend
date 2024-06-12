# Use uma imagem base do Python
FROM python:3.12

# Defina a variável de ambiente para o Python não criar arquivos pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Defina a variável de ambiente para o Python não bufferizar stdout e stderr
ENV PYTHONUNBUFFERED 1

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instale as dependências do sistema necessárias para o PostgreSQL
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean

# Copie o arquivo de requisitos e instale as dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copie o conteúdo do projeto para o contêiner
COPY . /app/

# Exponha a porta em que o Django vai rodar (por padrão 8000)
EXPOSE 8000

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
