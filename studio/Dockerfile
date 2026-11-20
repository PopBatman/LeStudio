FROM python:3.12.16-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --disable-pip-version-check --no-cache-dir --only-binary=:all: --require-hashes -r requirements.txt

COPY manage.py ./
COPY central/ central/
COPY workspace/ workspace/
COPY registre/ registre/
COPY raccordement/ raccordement/
COPY depots/ depots/
COPY composition/ composition/
COPY tests/ tests/
COPY work/items/FEAT-003-01/evidence/composition-v1.json work/items/FEAT-003-01/evidence/composition-v1.json
COPY templates/ templates/
COPY static/ui/ static/ui/
USER 10001:10001
CMD ["sh", "-ec", "python manage.py migrate --noinput && exec python manage.py runserver 0.0.0.0:8000 --noreload"]
