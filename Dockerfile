FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
