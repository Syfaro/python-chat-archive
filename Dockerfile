FROM python:3.11
WORKDIR /app
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --extras postgres && \
    rm -rf /root/.cache/pypoetry
COPY ./ ./
RUN poetry install --extras postgres
CMD ["poetry", "run", "chat-archive", "sync"]
