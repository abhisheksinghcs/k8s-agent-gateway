FROM --platform=$BUILDPLATFORM python:3.12.15-slim-bookworm@sha256:6a0e06f5ba0b373d051aabd3fffb9b873f27f9a2a3a14bcbe37dee6f0e3bbc70 AS requirements
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN printf '%s\n' 'uv==0.11.24 --hash=sha256:6ecdad43e870f88d3772d9d37e877259ae35ec374d51589805cdcf6196205829 --hash=sha256:e7e78c18686202c8b8715bebb83bfaf58f82d7fb848b6a5ae4e925a9fac3de4c --hash=sha256:48a6123f71b801e0e0b8a38520b011632ad81e0a043445044ce5b1a7b1cec7b6' \
    | python -m pip --isolated install --disable-pip-version-check --no-cache-dir --no-deps --only-binary=:all: \
    --index-url https://packagefeedproxy.microsoft.io/pypi/simple --require-hashes -r /dev/stdin \
    && uv export --offline --frozen --no-dev --no-emit-project --output-file requirements.txt

FROM python:3.12.15-slim-bookworm@sha256:6a0e06f5ba0b373d051aabd3fffb9b873f27f9a2a3a14bcbe37dee6f0e3bbc70
LABEL com.azure.containerizationassist.createdby="containerization-assist"
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_DEFAULT_INDEX=https://packagefeedproxy.microsoft.io/pypi/simple \
    PIP_CONFIG_FILE=/dev/null \
    PIP_INDEX_URL=https://packagefeedproxy.microsoft.io/pypi/simple \
    PIP_EXTRA_INDEX_URL="" \
    LAB_HOST=0.0.0.0
COPY --from=requirements /app/requirements.txt ./
RUN python -m venv .venv \
    && .venv/bin/python -m pip --isolated install --disable-pip-version-check --no-cache-dir --no-deps --only-binary=:all: \
        --index-url https://packagefeedproxy.microsoft.io/pypi/simple --require-hashes -r requirements.txt \
    && useradd --no-create-home --uid 10001 appuser
COPY main.py ./
COPY config/lab-info.json ./config/lab-info.json
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD ["/app/.venv/bin/python", "-c", "import urllib.request; urllib.request.build_opener(urllib.request.ProxyHandler({})).open('http://127.0.0.1:8000/healthz', timeout=3).close()"]
CMD ["/app/.venv/bin/python", "main.py"]