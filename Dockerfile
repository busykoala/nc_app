FROM alpine:latest as prod

RUN apk update && \
    apk add --no-cache \
        python3 \
        py3-pip \
        openssl

WORKDIR /app

# setup app & user space
RUN addgroup -S conncheck -g 1000
RUN adduser -H -S conncheck -G conncheck -h /app -s /bin/bash -u 1000
RUN chown conncheck:conncheck /app -R

USER conncheck

COPY . ${WORKDIR}

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    python3 -m poetry config virtualenvs.in-project true && \
    python3 -m poetry install --no-dev && \
    rm -rf ~/.cache/pypoetry/artifacts && rm -rf ~/.cache/pypoetry/cache
# ^ https://github.com/python-poetry/poetry/issues/6445

ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["python3", "-m", "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
