FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instale as dependências do sistema necessárias para o PostgreSQL
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean

# Adicione um novo grupo não privilegiado para utilizar no teste de integração
RUN addgroup nonroot

# Adicione um novo usuário não privilegiados
RUN useradd --no-log-init -r -g nonroot nonroot

# Copie o arquivo de requisitos e instale as dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

RUN chown -R nonroot:nonroot /app

EXPOSE 80

USER nonroot

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
