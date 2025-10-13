FROM alpine:3.20 AS prod

RUN apk add --no-cache \
  python3 \
  py3-pip \
  curl \
  openssl \
  ca-certificates

WORKDIR /app

# user with HOME at /app (as you had)
RUN addgroup -S conncheck -g 1000 && \
    adduser -H -S conncheck -G conncheck -h /app -s /bin/sh -u 1000 && \
    chown conncheck:conncheck /app -R

USER conncheck

# make sure installer targets /app and poetry is on PATH
ENV HOME=/app
ENV PATH="/app/.local/bin:${PATH}"

# install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3

# copy sources
COPY . .

# in-project venv and install deps
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PYTHONPATH=/app
RUN poetry --version && \
    poetry install --no-dev --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/*

EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
