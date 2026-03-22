# Alterado de volta para 3.12 para satisfazer o seu pyproject.toml
ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false

# Agora o poetry install vai funcionar porque a versão do Python será a 3.12
RUN poetry install --only main --no-root --no-interaction

COPY . /code

# Entra na pasta onde o manage.py realmente está
WORKDIR /code/CineReserve

# A SECRET_KEY idealmente deve vir do 'fly secrets set'
ENV SECRET_KEY "eQdyTnFLs5GufFUWAA3HgyHuWV81kLKeiyF9qVFSdDZp6dSgJW"

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Ajuste no caminho do WSGI
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "CineReserve.wsgi"]