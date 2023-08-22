FROM python:3.11
WORKDIR /app
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction && \
    rm -rf /root/.cache/pypoetry
COPY ./ ./
RUN poetry install
CMD ["poetry", "run", "chat-archive", "sync"]
