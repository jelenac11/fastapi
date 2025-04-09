# FastAPI

This project is demoing usage of FastAPI, SQLAlchemy and Pydantic.

## Prerequisites
1. Install poetry to manage dependencies
   ```sh
   pipx install poetry
   ```
2. Install docker and docker-compose <br>
   See docker Installation guide for your operating system [here](https://docs.docker.com/get-docker/)

## Installation manually (for local development)

0. First clone the repository from [the Cornelsen Git project](git@git.cornelsen.de:ai-platform/ai-process/exernice.git)

```bash
git clone git@github.com:jelenac11/fastapi.git
cd fastapi
```

1. Create a virtual environment and activate it

```bash
poetry env use python3.13
poetry shell
```

Your teminal should indicate with brackets, that you are inside the virtual environment (e.g. `(fastapi+sqlalchemy+pydantic-py3.13)`)

2. Install dependencies
```bash
poetry install --no-root --sync
```

3. Create local config

In the /root folder, create a file called `.env`. Configure the .env file
```bash
cp .env.dist .env
```

4. Run the app using uvicorn
```bash
cd src/
uvicorn main:app --port 8080 --reload --env-file ../.env
```

5. Run the app via docker: build docker containers (Docker must be installed on your machine)
```bash
docker compose build
```

6. run docker containers (Docker must be installed on your machine)
```bash
docker compose up
```

NOTE: There's  script in order to seed the db. First set database url as env var: DB_URL, and then run the following command to seed the db:
```bash
python scripts/seed.py
```

7. Access the app on localhost:8000

8. run tests to ensure everything works
```bash
pytest
```
NOTE: In order to run tests .env.test file should be created and configured.

## Development

The development dependencies are done via [poetry](https://python-poetry.org/).
All dependencies are defined in pyproject.toml, see [here](https://python-poetry.org/docs/pyproject/) for further information.
Ensure that development tooling like lint and tests are defined in the group `dev` in pyproject.toml

For adding packages use command:
```sh
poetry add (package)
```
For adding dev packages use command:
```sh
poetry add -G dev (package)
```

## Linting and formatting

[Ruff](https://docs.astral.sh/ruff/) is used as linter and as formatter.
Also, [mypy](https://mypy-lang.org/) is used for static type checking.

All these tools are integrated as part of pre-commit hooks.

Hooks will run on every commit. If you want to manually run pre-commit hooks, use command:
```bash
pre-commit run --all-files
```
