# Python version here
ARG PYTHON_VERSION=3.13
ARG POETRY_VERSION=1.8.4
ARG PYTHON_VENV="/app/.venv"


FROM python:${PYTHON_VERSION} AS builder
ARG POETRY_VERSION
ARG PYTHON_VENV
WORKDIR /app

# reduce python buffering and don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install poetry
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# Set environment varibales for poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# create & activate virtual env & install python deps
RUN python -m venv "${PYTHON_VENV}"
ENV PATH="${PYTHON_VENV}/bin:${PATH}"
COPY pyproject.toml poetry.lock* ./

RUN --mount=type=cache,target="${POETRY_CACHE_DIR}" \
    poetry install --only main,dev --no-root

# Add code
COPY /src ./src

# run with entrypoint and cmd (which allows for adjusting arguments at runtime)
ENTRYPOINT ["uvicorn", "--app-dir", "./src", "main:app", "--host", "0.0.0.0"]

EXPOSE 8080

