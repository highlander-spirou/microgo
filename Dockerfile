FROM python:3.10-slim
RUN pip install poetry==1.7.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY monolith ./monolith
RUN touch README.md

RUN poetry config virtualenvs.create false
RUN poetry install --only monolith

WORKDIR /app/monolith

ENTRYPOINT ["poetry", "run", "python", "index.py"]