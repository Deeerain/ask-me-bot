FROM python:3.12-alpine

RUN pip install poetry

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-root

COPY ./ask_me_bot /app/

CMD [ "poetry", "run", "python", "main.py" ]
