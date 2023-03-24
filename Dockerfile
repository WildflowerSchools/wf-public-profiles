FROM python:3.11-slim

RUN apt update -y && \
    apt install build-essential libpq-dev -y && \
    pip install poetry wheel --upgrade

WORKDIR /app

COPY poetry.lock pyproject.toml setup.py /app/

RUN poetry config virtualenvs.create false && poetry install --without dev --no-interaction --no-ansi  --no-root

COPY alembic.ini /app
COPY /alembic /app/alembic
COPY scripts/start_public_profiles_service.sh /app

ADD /wf_public_profiles /app/wf_public_profiles

CMD sh /app/start_public_profiles_service.sh

EXPOSE 4050  # This is ignored by Heroku, which assigns and exposes a random PORT