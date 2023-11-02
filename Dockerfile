FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11
ENV APP_PORT=5000
WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
COPY --from=requirements-stage /tmp/pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./app /app

CMD gunicorn --bind 0.0.0.0:${APP_PORT} --timeout 30 --access-logfile - app:app